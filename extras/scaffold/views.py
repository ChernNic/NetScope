from django.contrib.auth.models import Group, Permission
from django.urls import path, reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from .history_tables import generate_history_table
from .tables import generate_table
from .filters import generate_filter
from .forms import generate_modelform
from .base import EnhancedListMixin

def generate_crud_views(model, app_name: str = None, base_url: str = "", icon: str = None, custom_detail_view=None):
    model_name = model.__name__.lower()

    # --- Автоопределение app_name для встроенных моделей ---
    builtin_overrides = {
        "Group": "users",
        "Permission": "users",
    }

    resolved_app_name = app_name or builtin_overrides.get(model.__name__, model._meta.app_label)

    # --- Патчинг app_label и кастомные поля (например, icon) ---
    class PatchedMeta(model._meta.__class__):
        @property
        def app_label(self):
            return resolved_app_name

        @property
        def model_name(self):
            return model.__name__.lower()

        @property
        def crud_icon(self):
            return getattr(self, "_crud_icon", "fas fa-database")

    model._meta.__class__ = PatchedMeta
    model._meta._crud_icon = icon or "fas fa-database"

    # --- Классы CRUD ---
    table_class = generate_table(model, custom_detail_view)  # Передаем custom_detail_view в generate_table
    filter_class = generate_filter(model, exclude=["password"])
    form_class = generate_modelform(model)
    success_url = reverse_lazy(f"{resolved_app_name}:{model_name}_list")

    def post(self, request, *args, **kwargs):
        selected = request.POST.getlist("select")
        if "delete" in request.POST and selected:
            model.objects.filter(id__in=selected).delete()
            messages.success(request, "Удалено успешно")
        return redirect(".")

    ListView = type(
        f"{model.__name__}ListView",
        (EnhancedListMixin, SingleTableMixin, FilterView),
        {
            "model": model,
            "table_class": table_class,
            "filterset_class": filter_class,
            "template_name": "scaffold/list.html",
            "post": post,
            "get_context_data": lambda self, **kwargs: {
                **super(type(self), self).get_context_data(**kwargs),
                "history_table": generate_history_table(model.history.model)(
                    model.history.all().order_by("-history_date")
                ),
                "history_enabled": hasattr(model, "history"),
                "table_id": f"{model._meta.app_label}_{model._meta.model_name}_table",
                "history_table_id": f"{model._meta.app_label}_{model._meta.model_name}_history_table",
            },
        }
    )

    Create = type(
        f"{model.__name__}CreateView",
        (CreateView,),
        {
            "model": model,
            "form_class": form_class,
            "template_name": f"{resolved_app_name}/{model_name}_form.html",
            "success_url": success_url,
        }
    )

    Edit = type(
        f"{model.__name__}EditView",
        (UpdateView,),
        {
            "model": model,
            "form_class": form_class,
            "template_name": f"{resolved_app_name}/{model_name}_form.html",
            "success_url": success_url,
        }
    )

    Delete = type(
        f"{model.__name__}DeleteView",
        (DeleteView,),
        {
            "model": model,
            "success_url": success_url,
            "template_name": "confirm_delete.html",
        }
    )

    # Детальное представление объекта
    if custom_detail_view:
        DetailViewClass = custom_detail_view
    else:
        DetailViewClass = None

    # Список маршрутов
    urlpatterns = [
        path(base_url, ListView.as_view(), name=f"{model_name}_list"),
        path(base_url + "add/", Create.as_view(), name=f"{model_name}_add"),
        path(base_url + "<int:pk>/edit/", Edit.as_view(), name=f"{model_name}_edit"),
        path(base_url + "<int:pk>/delete/", Delete.as_view(), name=f"{model_name}_delete"),
    ]
    
    # Добавляем путь для детального представления только если оно задано
    if DetailViewClass:
        urlpatterns.append(path(base_url + "<int:pk>/", DetailViewClass.as_view(), name=f"{model_name}_detail"))

    return urlpatterns
