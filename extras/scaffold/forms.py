from django import forms
from django.db import models

from extras.scaffold.base_forms import BaseForm
from django.forms.models import inlineformset_factory
from django.db.models import ManyToOneRel


def generate_modelform(model_class):
    widgets = {}
    for field in model_class._meta.get_fields():
        if isinstance(field, models.ManyToManyField) and field.editable and not field.auto_created:
            widgets[field.name] = forms.CheckboxSelectMultiple()

    Meta = type('Meta', (), {
        'model': model_class,
        'fields': '__all__',
        'widgets': widgets,
    })

    return type('AutoForm', (BaseForm,), {'Meta': Meta})



def generate_inline_formsets(model):
    from django.core.exceptions import ImproperlyConfigured

    inlines = []

    for related in model._meta.related_objects:
        if isinstance(related, ManyToOneRel):
            related_model = related.related_model

            # Найдём все FK в related_model, указывающие на model
            fk_fields = [
                f for f in related_model._meta.fields
                if isinstance(f, models.ForeignKey) and f.remote_field.model == model
            ]

            if len(fk_fields) != 1:
                # Либо логируем, либо пропускаем
                continue

            parent_link_name = fk_fields[0].name
            fields = [
                f.name for f in related_model._meta.fields
                if f.editable and f.name != parent_link_name and f.name != "id"
            ]

            if not fields:
                continue

            FormSet = inlineformset_factory(
                model,
                related_model,
                fields=fields,
                extra=1,
                can_delete=True,
                fk_name=parent_link_name,  # <-- Указание нужного ForeignKey
            )
            inlines.append((related_model._meta.verbose_name_plural.title(), FormSet))

    return inlines
