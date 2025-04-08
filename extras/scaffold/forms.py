from django import forms
from django.db import models

from extras.scaffold.base_forms import BaseForm

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



