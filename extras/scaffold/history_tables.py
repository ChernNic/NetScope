import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

def generate_history_table(model_class):
    class HistoryTable(tables.Table):
        object_repr = tables.Column(verbose_name="Объект", empty_values=())

        def render_object_repr(self, record):
            try:
                instance = record.instance
                try:
                    instance.refresh_from_db()
                except model_class.DoesNotExist:
                    return format_html('<span class="text-error">Удалённый объект</span>')

                # Пытаемся безопасно получить строковое представление
                try:
                    obj = str(instance)
                except Exception:
                    obj = f"{instance._meta.verbose_name} #{instance.pk}"

                try:
                    url = reverse(
                        f"{instance._meta.app_label}:{instance._meta.model_name}_detail",
                        kwargs={"pk": instance.pk}
                    )
                    return format_html('<a href="{}" class="link link-primary break-all">{}</a>', url, obj)
                except Exception:
                    return format_html('<span class="text-warning break-all">{}</span>', obj)

            except Exception:
                raw = str(record)
                clean = raw.split(" as of ")[0]
                return format_html(
                    '<span class="text-error break-all cursor-not-allowed" title="Объект не существует">{}</span>',
                    clean or "—"
                )

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
            fields = ["object_repr", "history_id", "history_date", "history_type", "history_user"]
            attrs = {"class": "table table-zebra table-sm w-full bg-base-100"}

    return HistoryTable
