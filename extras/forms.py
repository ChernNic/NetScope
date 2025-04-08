from django import forms
from django.contrib.contenttypes.models import ContentType
from extras.scaffold.forms import BaseForm
from .models import Tag

class TagForm(BaseForm, forms.ModelForm):
    models = forms.ModelMultipleChoiceField(queryset=ContentType.objects.all(), required=False, label="Модели")

    class Meta:
        model = Tag
        fields = ['name', 'models']
        labels = {
            'name': 'Название тега',
            'models': 'Модели, к которым можно привязать тег',
        }
