from django.urls import path
from inventory.models import Organization, Building, Location, Device, Interface, Connection, DeviceRole, Manufacturer, DeviceType
from extras.scaffold import generate_crud_views
from inventory.views import *

app_name = "inventory"

urlpatterns = [
    *generate_crud_views(Organization, app_name="inventory", base_url="organizations/", icon="fas fa-building"),
    *generate_crud_views(Building, app_name="inventory", base_url="buildings/", icon="fas fa-warehouse"),
    *generate_crud_views(Location, app_name="inventory", base_url="locations/", icon="fas fa-map-marker-alt"),
    *generate_crud_views(Device, app_name="inventory", base_url="devices/", icon="fas fa-cogs"),
    *generate_crud_views(Interface, app_name="inventory", base_url="interfaces/", icon="fas fa-plug"),
    *generate_crud_views(Connection, app_name="inventory", base_url="connections/", icon="fas fa-random"),
    *generate_crud_views(DeviceRole, app_name="inventory", base_url="device_roles/", icon="fas fa-briefcase"),
    *generate_crud_views(Manufacturer, app_name="inventory", base_url="manufacturers/", icon="fas fa-industry"),
    *generate_crud_views(DeviceType, app_name="inventory", base_url="device_types/", icon="fas fa-laptop"),
    path("role_icons/", RoleIconListView.as_view(), name="roleicon_list"),
]
