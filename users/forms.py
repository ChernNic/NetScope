from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from extras.scaffold.base_forms import BaseForm

from .models import User

class CustomUserCreationForm(UserCreationForm, BaseForm):
    username = forms.CharField(label="Имя пользователя")
    email = forms.EmailField(label="Электронная почта")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)    

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

class CustomUserChangeForm(UserChangeForm, BaseForm):
    email = forms.EmailField(label="Электронная почта")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    role = forms.CharField(label="Роль пользователя")

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

class CustomAuthenticationForm(AuthenticationForm, BaseForm):
    """Форма входа с кастомными стилями"""
    
    username = forms.CharField(label="Электронная почта")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')