from django.urls import path
from extras.scaffold import generate_crud_views
from topology.views import NetworkMapDetailView, available_interfaces, create_connection, delete_connection_by_id, remove_device_from_map, save_device_position
from .models import NetworkMap

app_name = "topology"

urlpatterns = [
    *generate_crud_views(NetworkMap, app_name="topology", base_url="maps/", icon="fas fa-project-diagram", custom_detail_view=NetworkMapDetailView,),
    path("interfaces/available/", available_interfaces, name="available_interfaces"),
    path("connections/create/", create_connection, name="create_connection"),
    path("connections/delete_by_id/", delete_connection_by_id, name="delete_connection"),
    path("maps/<int:map_id>/save_position/", save_device_position, name="save_device_position"),
    path("maps/<int:map_id>/remove_device/", remove_device_from_map, name="remove_device"),
]