from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required

def register(request):
    """Регистрация нового пользователя"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home") 
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form_fieldset": form.render_as_fieldset(legend="Регистрация", submit_text="Зарегистрироваться")})

def user_login(request):
    """Авторизация пользователя"""
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = CustomAuthenticationForm()

    return render(request, "users/login.html", {"form_fieldset": form.render_as_fieldset(legend="Авторизация", submit_text="Войти")})

@login_required
def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect("users:login") 
