from django.utils.timezone import now
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from users.models import PasswordResetRequest, User
from .forms import AdminSetPasswordForm, CustomUserCreationForm, CustomAuthenticationForm, PasswordResetRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.templatetags.static import static
from django.db.models.fields.related import ForeignObjectRel
from .forms import AdminSetPasswordForm
from django.utils.timezone import now

def register(request):
    """Регистрация нового пользователя"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend' 
            login(request, user)
            return redirect("home") 
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {
        "form_fieldset": form.render_as_fieldset(legend="Регистрация", submit_text="Зарегистрироваться")
    })


def user_login(request):
    """Авторизация пользователя"""
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user.backend = 'django.contrib.auth.backends.ModelBackend' 
            login(request, user)
            return redirect("home")
    else:
        form = CustomAuthenticationForm()

    return render(request, "users/login.html", {
        "form_fieldset": form.render_as_fieldset(legend="Авторизация", submit_text="Войти")
    })


@login_required
def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect("users:login") 

def request_password_reset(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if not User.objects.filter(email=email).exists():
                messages.error(request, "Пользователь с таким email не найден.")
            elif PasswordResetRequest.objects.filter(email=email, approved=False).exists():
                messages.warning(request, "Запрос уже существует и ожидает обработки.")
            else:
                form.save()
                messages.success(request, "Запрос на смену пароля отправлен.")
                return redirect("users:login")
    else:
        form = PasswordResetRequestForm()
    return render(request, "users/password_reset_request.html", {
        "form_fieldset": form.render_as_fieldset(legend="Запрос на смену пароля", submit_text="Отправить запрос")
    })


@staff_member_required
def approve_password_reset(request, pk):
    obj = get_object_or_404(PasswordResetRequest, pk=pk)
    user = obj.user
    form = AdminSetPasswordForm(user=user, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        obj.approved = True
        obj.processed_at = now()
        obj.save()
        messages.success(request, f"Пароль для пользователя {user.email} успешно обновлён.")
        return redirect("users:passwordresetrequest_list")

    return render(request, "users/approve_password_reset.html", {
        "form_fieldset": form.render_as_fieldset(legend="Смена пароля пользователя", submit_text="Сменить пароль"),
        "user_email": user.email
    })

class PasswordResetRequestDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = PasswordResetRequest
    template_name = "scaffold/detail.html"
    context_object_name = "object"

    def test_func(self):
        return self.request.user.is_staff  # Только для администраторов

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = User.objects.get(email=self.object.email)

        form = AdminSetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            self.object.approved = True
            self.object.processed_at = now()
            self.object.save()
            messages.success(request, "Пароль успешно обновлён.")
            return redirect("users:passwordresetrequest_list")

        return self.get(request, form=form, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        user = User.objects.filter(email=obj.email).first()

        context["model_name"] = obj._meta.model_name
        context["app_label"] = obj._meta.app_label
        context["model_icon"] = getattr(obj._meta, "_crud_icon", "fas fa-key")
        context["object_icon_url"] = None  # нет иконки

        # Список полей
        context["fields"] = []
        for field in obj._meta.get_fields():
            if isinstance(field, ForeignObjectRel):
                continue
            value = getattr(obj, field.name, None)
            if field.many_to_one or field.one_to_one:
                context["fields"].append({
                    "name": field.verbose_name,
                    "value": str(value) if value else None,
                    "link": None,
                    "is_boolean": False,
                })
            elif field.many_to_many:
                context["fields"].append({
                    "name": field.verbose_name,
                    "value": list(value.all()) if value else None,
                    "link": None,
                    "is_boolean": False,
                    "is_list": True,
                })
            else:
                if field.choices:
                    display = getattr(obj, f"get_{field.name}_display")()
                else:
                    display = value
                context["fields"].append({
                    "name": field.verbose_name,
                    "value": display,
                    "link": None,
                    "is_boolean": isinstance(display, bool),
                })

        # Если заявка не одобрена — передаём форму
        if not obj.approved and user:
            form = kwargs.get("form") or AdminSetPasswordForm(user=user)
            context["form_fieldset"] = form.render_as_fieldset(legend="Установить новый пароль", submit_text="Сменить и одобрить")
        else:
            context["form_fieldset"] = None

        context["object_history"] = []

        return context