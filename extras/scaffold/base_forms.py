from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import re

class BaseForm(forms.ModelForm):
    PASSWORD_PATTERN = r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
    PASSWORD_HINT = """
        <p class="validator-hint hidden text-sm text-gray-500 mt-1" id="password-hint">
          Пароль должен содержать минимум 8 символов, включая:
          <br/>• хотя бы одну цифру
          <br/>• хотя бы одну строчную букву
          <br/>• хотя бы одну заглавную букву
        </p>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_classes = {
            forms.CharField: "input input-bordered w-full peer validator",
            forms.EmailField: "input input-bordered w-full peer validator",
            forms.PasswordInput: "input input-bordered w-full peer validator",
            forms.IntegerField: "input input-bordered w-full peer validator",
            forms.ChoiceField: "select select-bordered w-full peer validator",
            forms.BooleanField: "checkbox checkbox-primary",
            forms.CheckboxInput: "checkbox checkbox-primary",
            forms.Textarea: "textarea textarea-bordered w-full peer validator",
        }

        for field_name, field in self.fields.items():
            widget = field.widget

            # Пропускаем CheckboxSelectMultiple — обрабатываем кастомно
            if isinstance(widget, forms.CheckboxSelectMultiple):
                widget.attrs["class"] = "checkbox checkbox-sm"
                continue

            widget.attrs["class"] = field_classes.get(type(field), "input input-bordered w-full peer validator")
            widget.attrs["placeholder"] = " "
            widget.attrs["required"] = False

            if isinstance(widget, forms.PasswordInput):
                widget.attrs["pattern"] = self.PASSWORD_PATTERN
                widget.attrs["title"] = "Пароль должен содержать минимум 8 символов, включая цифру, строчную и заглавную букву."


    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            return password
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну строчную букву.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
        return password

    def render_password_field(self, field, show_hint=False):
        hint_html = self.PASSWORD_HINT if show_hint else ""
        help_text_html = f'<p class="text-sm text-gray-500 mt-1">{field.help_text}</p>' if field.help_text else ""
        return mark_safe(f"""
            <label class="fieldset-label">{field.label}</label>
            {field}
            {help_text_html}
            {hint_html}
        """)

    def render_as_fieldset(self, legend=None, submit_text=None, submit_class="btn btn-neutral mt-4"):
        is_filter_form = not hasattr(self, "_meta") or not hasattr(self._meta, "model")
        password_fields = [name for name, field in self.fields.items() if isinstance(field.widget, forms.PasswordInput)]
        first_password_rendered = False

        if not legend:
            if is_filter_form:
                legend = "Фильтрация"
            else:
                try:
                    model = self._meta.model
                    name = model.get_verbose_accusative() if hasattr(model, "get_verbose_accusative") else model._meta.verbose_name
                    is_create = getattr(self, "instance", None) is None or getattr(self.instance, "pk", None) is None
                    legend = f"{'Создание' if is_create else 'Редактирование'} {name}"
                except Exception:
                    legend = "Форма"

        if not submit_text:
            submit_text = "Найти" if is_filter_form else "Сохранить"

        output = f'<fieldset class="fieldset w-full bg-base-200 border border-base-300 p-4 rounded-box">'
        output += f'<legend class="fieldset-legend mb-2">{legend}</legend>'

        for field in self:
            if field.name in password_fields:
                output += self.render_password_field(field, show_hint=not first_password_rendered)
                first_password_rendered = True

            elif isinstance(field.field.widget, forms.CheckboxSelectMultiple):
                output += f'''
                <label class="fieldset-label">{field.label}</label>
                <div class="overflow-y-auto max-h-64 border border-base-300 rounded-lg p-2 bg-base-100">
                  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                '''
                for subwidget in field:
                    output += format_html(
                        '''
                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" name="{}" value="{}" {} class="multi-checkbox checkbox checkbox-primary checkbox-xs" id="{}" data-field="{}" />
                            <span class="label-text">{}</span>
                        </label>
                        ''',
                        field.name,  # Уникальное имя для группы чекбоксов
                        subwidget.data["value"],
                        "checked" if subwidget.data["selected"] else "",
                        subwidget.id_for_label,
                        field.name,  # Используем data-field с именем поля
                        subwidget.choice_label,
                    )

                output += '''
                  </div>
                </div>
                <div class="mt-2">
                    <button type="button" class="btn btn-sm btn-outline btn-info mr-2"
                            onclick="toggleAllCheckboxes('{}', true)">
                        Выделить все
                    </button>
                    <button type="button" class="btn btn-sm btn-outline btn-error"
                            onclick="toggleAllCheckboxes('{}', false)">
                        Убрать все
                    </button>
                </div>
                '''.format(field.name, field.name)  # Передаем имя поля в кнопку

            else:
                output += f'''
                <label class="fieldset-label">{field.label}</label>
                {field}
                '''
                if field.help_text:
                    output += f'<p class="text-sm text-gray-500 mt-1">{field.help_text}</p>'

            if field.errors:
                output += f'<p class="text-error">{field.errors}</p>'

        output += f'<button type="submit" class="{submit_class}">{submit_text}</button>'
        output += '</fieldset>'

        # JS для выделения/снятия всех чекбоксов
        output += mark_safe("""
        <script>
            function toggleAllCheckboxes(fieldName, checked) {
                document.querySelectorAll(`input.multi-checkbox[data-field="${fieldName}"]`).forEach(cb => {
                    cb.checked = checked;
                });
            }
        </script>
        """)

        return mark_safe(output)


class BasePureForm(forms.Form):
    PASSWORD_PATTERN = r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
    PASSWORD_HINT = """
        <p class="validator-hint hidden text-sm text-gray-500 mt-1" id="password-hint">
          Пароль должен содержать минимум 8 символов, включая:
          <br/>• хотя бы одну цифру
          <br/>• хотя бы одну строчную букву
          <br/>• хотя бы одну заглавную букву
        </p>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_classes = {
            forms.CharField: "input input-bordered w-full",
            forms.EmailField: "input input-bordered w-full",
            forms.PasswordInput: "input input-bordered w-full",
            forms.IntegerField: "input input-bordered w-full",
            forms.ChoiceField: "select select-bordered w-full",
            forms.BooleanField: "checkbox checkbox-primary",
            forms.CheckboxInput: "checkbox checkbox-primary",
            forms.Textarea: "textarea textarea-bordered w-full",
        }

        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxSelectMultiple):
                widget.attrs["class"] = "checkbox checkbox-sm"
                continue

            # Присваиваем классы и плейсхолдер
            widget.attrs["class"] = field_classes.get(type(field), "input input-bordered w-full")
            widget.attrs["placeholder"] = field.label
            widget.attrs.setdefault("required", False)

            if isinstance(widget, forms.PasswordInput):
                widget.attrs["pattern"] = self.PASSWORD_PATTERN
                widget.attrs["title"] = "Пароль должен содержать минимум 8 символов, включая цифру, строчную и заглавную букву."


    def render_password_field(self, field, show_hint=False):
        help_text_html = f'<p class="text-sm text-gray-500 mt-1">{field.help_text}</p>' if field.help_text else ""
        hint_html = self.PASSWORD_HINT if show_hint else ""
        return mark_safe(f"""
            <label class="fieldset-label">{field.label}</label>
            {field}
            {help_text_html}
            {hint_html}
        """)

    def render_as_fieldset(self, legend=None, submit_text="Отправить", submit_class="btn btn-neutral mt-4"):
        password_fields = [name for name, field in self.fields.items() if isinstance(field.widget, forms.PasswordInput)]
        first_password_rendered = False

        output = f'<fieldset class="fieldset w-full bg-base-200 border border-base-300 p-4 rounded-box">'
        output += f'<legend class="fieldset-legend mb-2">{legend or "Форма"}</legend>'

        for field in self:
            if field.name in password_fields:
                output += self.render_password_field(field, show_hint=not first_password_rendered)
                first_password_rendered = True
            else:
                output += f'<label class="fieldset-label">{field.label}</label>{field}'
                if field.help_text:
                    output += f'<p class="text-sm text-gray-500 mt-1">{field.help_text}</p>'
            if field.errors:
                output += f'<p class="text-error">{field.errors}</p>'

        output += f'<button type="submit" class="{submit_class}">{submit_text}</button></fieldset>'
        return mark_safe(output)
