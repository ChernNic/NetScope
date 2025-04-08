from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    
    class Meta:
        abstract = True

    @classmethod
    def get_verbose_accusative(cls):
        meta = cls._meta
        name = getattr(meta, "verbose_name", cls.__name__.lower())
        return cls.inflect(name, "accs")

    @staticmethod
    def inflect(word, target_case: str):
        from pymorphy2 import MorphAnalyzer
        morph = MorphAnalyzer()
        parsed = morph.parse(word)[0]
        inflected = parsed.inflect({target_case})
        return inflected.word if inflected else word
