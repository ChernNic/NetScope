from django.urls import path
from ipam.models import Subnet, VLAN, VRF
from extras.scaffold import generate_crud_views

app_name = "ipam"

urlpatterns = [
    *generate_crud_views(Subnet, app_name="ipam", base_url="subnets/", icon="fas fa-route"),
    *generate_crud_views(VLAN, app_name="ipam", base_url="vlans/", icon="fas fa-layer-group"),
    *generate_crud_views(VRF, app_name="ipam", base_url="vrfs/", icon="fas fa-random"),
]
