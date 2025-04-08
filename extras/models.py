from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _

from extras.scaffold.models import BaseModel

class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Имя"))
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("тег")
        verbose_name_plural = _("теги")


# Модель CustomField, также наследующая от BaseModel
class CustomField(BaseModel):
    FIELD_TYPES = [
        ('char', _('CharField')),
        ('int', _('IntegerField')),
        ('date', _('DateField')),
        ('boolean', _('BooleanField')),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_("Название поля"), null=True)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPES, verbose_name=_("Тип данных"), null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Тип объекта"), null=True)
    object_id = models.PositiveIntegerField(verbose_name=_("ID объекта"), null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("кастомное поле")
        verbose_name_plural = _("кастомные поля")