import django_tables2 as tables

class BaseTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="extras/actions_column.html",
        orderable=False,
        verbose_name="Действия",
    )

    class Meta:
        template_name = "django_tables2/daisy.html" 
        attrs = {
            "class": "table table-zebra table-sm bg-base-100 w-full"
        }

