from django.urls import path
from users.models import CustomGroup, User
from extras.scaffold import generate_crud_views
from .views import register, user_login, user_logout

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    *generate_crud_views(User, app_name="users", base_url="users/", icon="fas fa-user"),
    *generate_crud_views(CustomGroup, app_name="users", base_url="groups/", icon="fas fa-users"),
]
