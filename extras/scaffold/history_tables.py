import django_tables2 as tables
from django.utils.html import format_html

def generate_history_table(model_class):
    """
    Генерирует таблицу истории с кастомным отображением типа действия и датой.
    """
    class Meta:
        model = model_class
        fields = ["history_id", "history_date", "history_type", "history_user"]
        attrs = {"class": "table table-zebra table-sm w-full bg-base-100"}

    class HistoryTable(tables.Table):
        history_id = tables.Column(verbose_name="ID")
        history_date = tables.DateTimeColumn(
            verbose_name="Дата изменения",
            accessor="history_date",
            format="d.m.Y H:i"
        )
        history_user = tables.Column(verbose_name="Пользователь")
        history_type = tables.Column(verbose_name="Тип")

        def render_history_type(self, record):
            value = record.history_type
            badge_class = {
                "+": "badge-success",
                "~": "badge-info",
                "-": "badge-error",
            }.get(value, "badge-neutral")

            label = {
                "+": "Создано",
                "~": "Изменено",
                "-": "Удалено",
            }.get(value, value)

            return format_html(
                '<div class="badge badge-outline {}">{}</div>',
                badge_class,
                label,
            )

        class Meta:
            model = model_class
            fields = ["history_id", "history_date", "history_type", "history_user"]
            attrs = {"class": "table table-zebra table-sm w-full bg-base-100"}

    return HistoryTable
