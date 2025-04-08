from django_tables2 import RequestConfig
from django.urls import reverse_lazy

class EnhancedListMixin:
    def get_table_data(self):
        self.filterset = self.filterset_class(self.request.GET, queryset=self.model.objects.all())
        return self.filterset.qs

    def get_table(self, **kwargs):
        table_class = self.get_table_class()
        table = table_class(self.get_table_data()) 
        RequestConfig(self.request, paginate={"per_page": 25}).configure(table)
        return table

    def get_table_class(self):
        return self.table_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_verbose_name_plural"] = self.model._meta.verbose_name_plural
        context["add_url"] = reverse_lazy(f"{self.model._meta.app_label}:{self.model._meta.model_name}_add")
        context["filter"] = getattr(self, "filterset", None)
        context["table_id"] = f"{self.model._meta.app_label}_{self.model._meta.model_name}"
        context["model_icon"] = getattr(self.model._meta, "crud_icon", "fas fa-database")

        return context
