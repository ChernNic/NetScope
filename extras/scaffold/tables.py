import django_tables2 as tables
from django.utils.html import format_html
from django.urls import NoReverseMatch, reverse

def generate_table(
    model_class,
    custom_detail_view=None,
    exclude=None,
    field_labels=None,
    custom_columns=None,
    column_overrides=None,
    order_by=None  
):
    exclude = exclude or []
    field_labels = field_labels or {}
    custom_columns = custom_columns or {}
    column_overrides = column_overrides or {}

    field_names = [f.name for f in model_class._meta.fields if f.name not in exclude]

    class Meta:
        model = model_class
        template_name = "django_tables2/daisy.html"
        fields = field_names
        attrs = {
            "class": "table table-zebra table-sm w-full bg-base-100"
        }
        ordering = order_by or ()

    # Базовые колонки
    table_fields = {
        "select": tables.CheckBoxColumn(accessor="pk", orderable=False),
        "actions": tables.Column(verbose_name="⋮", accessor="pk", orderable=False),
        "Meta": Meta,
    }

    # Рендерим actions как иконки
    def render_actions(self, record):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        app = model_class._meta.app_label
        model = model_class.__name__.lower()

        perms = {
            "view": f"{app}.view_{model}",
            "change": f"{app}.change_{model}",
            "delete": f"{app}.delete_{model}",
        }

        try:
            view_url = reverse(f"{app}:{model}_detail", kwargs={"pk": record.pk}) if user.has_perm(perms["view"]) else None
        except NoReverseMatch:
            view_url = None

        try:
            edit_url = reverse(f"{app}:{model}_edit", kwargs={"pk": record.pk}) if user.has_perm(perms["change"]) else None
        except NoReverseMatch:
            edit_url = None

        try:
            delete_url = reverse(f"{app}:{model}_delete", kwargs={"pk": record.pk}) if user.has_perm(perms["delete"]) else None
        except NoReverseMatch:
            delete_url = None

        if not any([view_url, edit_url, delete_url]):
            return ""

        return format_html(
            '''
            <div class="flex items-center gap-1 text-sm leading-tight">
                {}
                {}
                {}
            </div>
            ''',
            format_html(
                '<a href="{}" class="inline-flex items-center justify-center rounded p-1 hover:bg-base-200 transition" title="Просмотр"><i class="fas fa-eye text-secondary text-xs"></i></a>',
                view_url,
            ) if view_url else '',
            format_html(
                '<a href="{}" class="inline-flex items-center justify-center rounded p-1 hover:bg-base-200 transition" title="Редактировать"><i class="fas fa-pen-to-square text-primary text-xs"></i></a>',
                edit_url,
            ) if edit_url else '',
            format_html(
                '<a href="{}" class="inline-flex items-center justify-center rounded p-1 hover:bg-error/10 transition" title="Удалить"><i class="fas fa-trash text-error text-xs"></i></a>',
                delete_url,
            ) if delete_url else '',
        )
        return actions

    # Добавляем field_labels
    for field in field_names:
        if field in field_labels:
            table_fields[field] = tables.Column(verbose_name=field_labels[field])

    # Добавляем column overrides
    for field, column in column_overrides.items():
        table_fields[field] = column

    # Добавляем кастомные колонки
    for key, column in custom_columns.items():
        table_fields[key] = column

    # Добавляем рендеринг для поля tags (ManyToMany)
    if 'tags' in model_class._meta.fields_map:
        def render_tags(self, record):
            # Получаем связанные теги
            tags = getattr(record, 'tags').all()  # Получаем все связанные теги
            # Преобразуем их в строку
            tag_names = [str(tag) for tag in tags]
            return format_html(", ".join(tag_names))

        # Добавляем колонку для тегов
        table_fields['tags'] = tables.Column(
            verbose_name="Теги",
            accessor='tags',  # Можно также указать accessor, если нужно специфическое поле
            render_func=render_tags,
            orderable=False
        )

    # Добавляем метод render_actions
    table_fields["render_actions"] = render_actions

    # Создаём таблицу
    TableClass = type(
        f"{model_class.__name__}Table",
        (tables.Table,),
        {**table_fields, "render_actions": render_actions}
    )

    return TableClass
