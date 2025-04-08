from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from extras.scaffold.models import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email обязателен'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser, BaseModel):

    history = HistoricalRecords()

    email = models.EmailField(
        unique=True,
        verbose_name=_("Электронная почта"),
        help_text=_("Введите действительный email")
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name=_("Имя")
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name=_("Фамилия")
    )
    
    role = models.CharField(
        max_length=50,
        choices=[
            ('admin', _("Администратор")),
            ('user', _("Пользователь"))
        ],
        default='user',
        verbose_name=_("Роль")
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class CustomGroup(Group):
    history = HistoricalRecords()

    class Meta:
        proxy = True
        verbose_name = "группа"
        verbose_name_plural = "группы"