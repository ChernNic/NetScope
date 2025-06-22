from django.contrib.auth.models import Group, Permission
from django.urls import path, reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.fields.related import ForeignObjectRel
from django.templatetags.static import static
from django.contrib.auth.mixins import PermissionRequiredMixin
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse


from typing import Optional

from .history_tables import generate_history_table
from .tables import generate_table
from .filters import generate_filter, generate_history_filter
from .forms import generate_inline_formsets, generate_modelform
from .base import EnhancedListMixin




def generate_crud_views(
    model,
    app_name: str = None,
    base_url: str = "",
    icon: str = None,
    custom_detail_view=None,
    enable_create=True,
    enable_edit=True,
    enable_delete=True,
    template_tabs: Optional[list[dict]] = None,  
):
    model_name = model.__name__.lower()

    builtin_overrides = {
        "Group": "users",
        "Permission": "users",
    }

    resolved_app_name = app_name or builtin_overrides.get(model.__name__, model._meta.app_label)

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

    table_class = generate_table(model, custom_detail_view)
    filter_class = generate_filter(model, exclude=["password"])
    form_class = generate_modelform(model)
    inline_formsets = generate_inline_formsets(model)

    success_url = reverse_lazy(f"{resolved_app_name}:{model_name}_list")

    def post(self, request, *args, **kwargs):
        selected = request.POST.getlist("select")
        if "delete" in request.POST and selected:
            model.objects.filter(id__in=selected).delete()
            messages.error(request, "Выбранные объекты удалены.")
        elif "import_json" in request.POST:
            json_file = request.FILES.get("json_file")
            if not json_file:
                return HttpResponse("Файл не выбран", status=400)
            try:
                import json
                from django.core.exceptions import ValidationError

                data = json.load(json_file)
                if not isinstance(data, list):
                    raise ValidationError("Ожидался список объектов.")

                for item in data:
                    instance = model(**item)
                    instance.save()

                messages.success(request, "Импорт завершён успешно.")
                return redirect(".")
            except Exception as e:
                return HttpResponse(f"Ошибка при импорте: {str(e)}", status=500)
        return redirect(".")


    def get(self, request, *args, **kwargs):
        if request.GET.get("export") == "json":
            import json
            from django.core.serializers.json import DjangoJSONEncoder
            from django.http import HttpResponse

            model_cls = self.model  
            model_name = model_cls._meta.model_name

            data = list(model_cls.objects.all().values())
            response = HttpResponse(
                json.dumps(data, cls=DjangoJSONEncoder),
                content_type="application/json"
            )
            response["Content-Disposition"] = f'attachment; filename="{model_name}_data.json"'
            return response

        return super(type(self), self).get(request, *args, **kwargs)

    def export_json(self, request):
        if request.GET.get("export") == "json":
            data = list(self.model.objects.all().values())
            response = HttpResponse(
                json.dumps(data, cls=DjangoJSONEncoder),
                content_type="application/json"
            )
            response["Content-Disposition"] = f'attachment; filename="{self.model._meta.model_name}.json"'
            return response


    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        obj_model = model
        context["model_name"] = obj_model._meta.model_name
        context["app_label"] = obj_model._meta.app_label
        context["model_icon"] = getattr(obj_model._meta, "_crud_icon", "fas fa-database")
        context["inlines"] = [(name, fs(self.request.POST or None)) for name, fs in inline_formsets]

        context["table_id"] = f"{obj_model._meta.app_label}_{obj_model._meta.model_name}_table"

        if hasattr(obj_model, "history"):
            history_model = obj_model.history.model
            history_qs = history_model.objects.all().order_by("-history_date")
            history_filter_class = generate_history_filter(history_model)
            history_filter = history_filter_class(self.request.GET, queryset=history_qs)
            history_table_class = generate_history_table(history_model)
            history_table = history_table_class(history_filter.qs)

            context["history_table"] = history_table
            context["history_filter"] = history_filter
            context["history_enabled"] = True
            context["history_table_id"] = f"{obj_model._meta.app_label}_{obj_model._meta.model_name}_history_table"
        else:
            context["history_enabled"] = False
            context["history_table"] = None
            context["history_filter"] = None

        context["enable_create"] = enable_create
        context["enable_edit"] = enable_edit
        context["enable_delete"] = enable_delete
        context["template_tabs"] = template_tabs or []  

        return context

    ListView = type(
        f"{model.__name__}ListView",
        (PermissionRequiredMixin, EnhancedListMixin, LoginRequiredMixin, SingleTableMixin, FilterView),
        {
            "model": model,
            "table_class": table_class,
            "filterset_class": filter_class,
            "template_name": "scaffold/list.html",
            "post": post,
            "get": lambda self, request, *args, **kwargs: (
                export_json(self, request) or super(type(self), self).get(request, *args, **kwargs)
            ),
            "get_context_data": get_context_data,
            "raise_exception": True,
            "permission_required": f"{resolved_app_name}.view_{model_name}",
            "_export_json": lambda self, request: (
                HttpResponse(
                    json.dumps(list(self.model.objects.all().values()), cls=DjangoJSONEncoder),
                    content_type="application/json"
                )
                if request.GET.get("export") == "json"
                else None
            )
        }
    )

    Create = type(
        f"{model.__name__}CreateView",
        (PermissionRequiredMixin, LoginRequiredMixin, CreateView),
        {
            "model": model,
            "form_class": form_class,
            "template_name": f"{resolved_app_name}/{model_name}_form.html",
            "success_url": success_url,
            "raise_exception": True,
            "permission_required": f"{resolved_app_name}.add_{model_name}",
            "form_valid": lambda self, form: (
                messages.success(self.request, f"Объект «{form.instance}» успешно создан."),
                super(type(self), self).form_valid(form)
            )[1],

            "get_initial": lambda self: {
                **super(type(self), self).get_initial(),
                **{
                    k: v
                    for k, v in self.request.GET.items()
                    if k in {f.name for f in self.model._meta.fields}
                },
            },

            "get_success_url": lambda self: (
                self.request.GET.get("next") or
                self.success_url
            ),
        }
    )

    Edit = type(
        f"{model.__name__}EditView",
        (PermissionRequiredMixin, UpdateView, LoginRequiredMixin),
        {
            "model": model,
            "form_class": form_class,
            "template_name": f"{resolved_app_name}/{model_name}_form.html",
            "form_valid": lambda self, form: (
                messages.info(self.request, f"Изменения для «{form.instance}» сохранены."),
                super(type(self), self).form_valid(form)
            )[1],
            "success_url": success_url,
            "raise_exception": True,
            "permission_required": f"{resolved_app_name}.change_{model_name}",
        }
    )

    Delete = type(
        f"{model.__name__}DeleteView",
        (PermissionRequiredMixin, DeleteView, LoginRequiredMixin),
        {
            "model": model,
            "success_url": success_url,
            "template_name": "confirm_delete.html",
            "raise_exception": True,
            "form_valid": lambda self, form: (
                messages.error(self.request, f"Объект «{self.get_object()}» удалён."),
                super(type(self), self).form_valid(form)
            )[1],
            "permission_required": f"{resolved_app_name}.delete_{model_name}",
        }
    )

    if custom_detail_view:
        DetailViewClass = custom_detail_view
    else:
        DetailViewClass = type(
            f"{model.__name__}DetailView",
            (AutoDetailView,),
            {
                "model": model,
                "extra_tabs": template_tabs or [],
            }
        )
        
    urlpatterns = [
        path(base_url, ListView.as_view(), name=f"{model_name}_list"),
    ]

    if enable_create:
        urlpatterns.append(path(base_url + "add/", Create.as_view(), name=f"{model_name}_add"))
    if enable_edit:
        urlpatterns.append(path(base_url + "<int:pk>/edit/", Edit.as_view(), name=f"{model_name}_edit"))
    if enable_delete:
        urlpatterns.append(path(base_url + "<int:pk>/delete/", Delete.as_view(), name=f"{model_name}_delete"))

    if DetailViewClass:
        urlpatterns.append(path(base_url + "<int:pk>/", DetailViewClass.as_view(), name=f"{model_name}_detail"))

    return urlpatterns


class AutoDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = "scaffold/detail.html"
    context_object_name = "object"
    extra_tabs = []

    raise_exception = True

    def get_extra_tabs(self):
        return self.extra_tabs

    def get_queryset(self):
        return self.model.objects.all()

    @property
    def permission_required(self):
        return f"{self.model._meta.app_label}.view_{self.model._meta.model_name}"

    def _resolve_icon_url(self, obj) -> Optional[str]:
        url = getattr(obj, "icon_url", None)
        if url:
            return url
        icon = getattr(obj, "icon", None)
        if icon and getattr(icon, "file_name", None):
            return static(f"icons/roles/{icon.file_name}")
        role = getattr(obj, "role", None) or getattr(obj, "device_role", None)
        if role and hasattr(role, "icons"):
            first_icon = role.icons.first()
            if first_icon:
                return static(f"icons/roles/{first_icon.file_name}")
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        context.update({
            "model_name": obj._meta.model_name,
            "app_label": obj._meta.app_label,
            "model_icon": getattr(obj._meta, "_crud_icon", "fas fa-database"),
            "object_icon_url": self._resolve_icon_url(obj),
            "extra_tabs": self.extra_tabs,
        })

        history_model = getattr(obj._meta.model, "history", None)
        context["object_history"] = history_model.filter(id=obj.id).order_by("-history_date") if history_model else []

        context["fields"] = []
        for field in self.object._meta.get_fields():
            if isinstance(field, ForeignObjectRel):
                continue
            value = getattr(self.object, field.name, None)
            if field.many_to_one or field.one_to_one:
                context["fields"].append({
                    "name": field.verbose_name,
                    "value": str(value) if value else None,
                    "link": reverse_lazy(f"{value._meta.app_label}:{value._meta.model_name}_detail", kwargs={"pk": value.pk}) if value else None,
                    "is_boolean": False,
                })
            elif field.many_to_many:
                value_list = list(value.all()) if value else None
                context["fields"].append({
                    "name": field.verbose_name,
                    "value": value_list,
                    "link": None,
                    "is_boolean": False,
                    "is_list": True,
                })
            elif hasattr(field, 'verbose_name'):
                display_value = getattr(self.object, f"get_{field.name}_display")() if field.choices else value
                context["fields"].append({
                    "name": field.verbose_name,
                    "value": display_value,
                    "link": None,
                    "is_boolean": isinstance(display_value, bool),
                })

        return context