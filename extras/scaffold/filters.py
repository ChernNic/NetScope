import django_filters
from django.db import models
from django import forms
from django.utils.safestring import mark_safe


def generate_filter(model_class, exclude=None):
    exclude = set(exclude or [])
    default_exclude = {"password", "last_login", "created_at", "updated_at"}
    exclude.update(default_exclude)

    field_overrides = {}

    def apply_widget_attrs(filter_instance):
        widget = filter_instance.field.widget
        field_class = type(filter_instance.field)

        classes = {
            forms.CharField: "input input-bordered w-full",
            forms.EmailField: "input input-bordered w-full",
            forms.IntegerField: "input input-bordered w-full",
            forms.ChoiceField: "select select-bordered w-full",
            forms.BooleanField: "select select-bordered w-full",
            forms.CheckboxInput: "select select-bordered w-full",
            forms.DateField: "input input-bordered w-full",
            forms.DateTimeField: "input input-bordered w-full",
        }

        css_class = next(
            (cls for base, cls in classes.items() if isinstance(filter_instance.field, base)),
            "input input-bordered w-full"
        )
        widget.attrs.update({
            "class": css_class,
            "placeholder": filter_instance.label or "",
            "required": False,
        })

    for field in model_class._meta.fields:
        if not isinstance(field.name, str) or field.name in exclude:
            continue

        internal_type = field.get_internal_type()
        label = (field.verbose_name or field.name).capitalize()

        if internal_type in ["CharField", "TextField", "EmailField"]:
            f = django_filters.CharFilter(lookup_expr="icontains", label=label)

        elif internal_type in ["IntegerField", "BigIntegerField", "SmallIntegerField"]:
            f = django_filters.NumberFilter(lookup_expr="exact", label=label)

        elif internal_type in ["BooleanField", "NullBooleanField"]:
            f = django_filters.BooleanFilter(
                label=label,
                widget=forms.Select(choices=[
                    ("", "---------"),
                    (True, "Да"),
                    (False, "Нет"),
                ])
            )

        elif internal_type in ["DateTimeField", "DateField"]:
            f = django_filters.DateFilter(lookup_expr="exact", label=label)

        elif isinstance(field, models.ForeignKey):
            f = django_filters.ModelChoiceFilter(
                queryset=field.related_model.objects.all(),
                label=label
            )

        else:
            f = django_filters.Filter(lookup_expr="exact", label=label)

        field_overrides[field.name] = f

    # Удаление мусора и установка стилей
    declared_filters = {
        name: f for name, f in field_overrides.items()
        if isinstance(name, str) and name != "None"
    }

    for f in declared_filters.values():
        apply_widget_attrs(f)

    def filter_init(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
        elif args:
            data = args[0]
            args = args[1:]
        else:
            data = None

        if data:
            data = data.copy()
            for key in list(data.keys()):
                value = data.get(key)
                if key not in declared_filters or value in ["", None, "unknown", "undefined", "null", "None"]:
                    data.pop(key)
                    continue

                f = declared_filters.get(key)
                if isinstance(f, django_filters.BooleanFilter):
                    if value == "true":
                        data[key] = True
                    elif value == "false":
                        data[key] = False
            kwargs["data"] = data

        super(AutoFilter, self).__init__(*args, **kwargs)

    def render_as_grid(self, submit_text="Найти", submit_class="btn btn-outline btn-sm"):
        form = self.form
        output = '<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">'
        for field in form.visible_fields():
            output += f'''
            <div class="form-control filter-field" data-filter-field="{field.name}">
                <label class="label">
                    <span class="label-text">{field.label}</span>
                </label>
                {field}
                {''.join(f'<p class="text-error">{e}</p>' for e in field.errors)}
                {f'<p class="text-sm text-gray-500 mt-1">{field.help_text}</p>' if field.help_text else ''}
            </div>
            '''
        output += f'''
        <div class="form-control col-span-full">
          <div class="join">
            <button type="submit" class="{submit_class} join-item">
              <i class="fas fa-search mr-1"></i> {submit_text}
            </button>
            <a href="?" class="btn btn-outline btn-sm join-item">
              <i class="fas fa-xmark mr-1"></i> Сбросить
            </a>
          </div>
        </div>
        </div>
        '''
        return mark_safe(output)

    AutoFilter = type(
        f"{model_class.__name__}AutoFilter",
        (django_filters.FilterSet,),
        {
            **declared_filters,
            "Meta": type("Meta", (), {
                "model": model_class,
                "fields": list(declared_filters.keys())
            }),
            "__init__": filter_init,
            "render_as_grid": render_as_grid,
        }
    )

    return AutoFilter
