from django.urls import path
from extras.models import Tag, CustomField
from extras.scaffold import generate_crud_views

app_name = "extras"

urlpatterns = [
    *generate_crud_views(Tag, app_name="extras", base_url="tags/", icon="fas fa-tag"),
    *generate_crud_views(CustomField, app_name="extras", base_url="customfields/", icon="fas fa-cogs"),
]