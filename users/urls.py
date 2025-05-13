from django.urls import path
from users.models import CustomGroup, PasswordResetRequest, User
from extras.scaffold import generate_crud_views
from .views import PasswordResetRequestDetailView, approve_password_reset, register, request_password_reset, user_login, user_logout

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    
    *generate_crud_views(User, app_name="users", base_url="users/", icon="fas fa-user"),
    *generate_crud_views(CustomGroup, app_name="users", base_url="groups/", icon="fas fa-users"),
    path("password-reset-request/", request_password_reset, name="password_reset_request"),
    path("password-reset-request/<int:pk>/approve/", approve_password_reset, name="password_reset_approve"),
    *generate_crud_views(PasswordResetRequest, 
                         app_name="users", 
                         base_url="resetrequests/", 
                         icon="fas fa-key",
                         custom_detail_view=PasswordResetRequestDetailView, 
                         enable_edit=False, 
                         enable_delete=False),
    
]
