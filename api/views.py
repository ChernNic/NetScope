from rest_framework import viewsets, generics
from users.models import User, CustomGroup
from ipam.models import VLAN, VRF, Subnet
from inventory.models import (
    Organization, Building, Location, Manufacturer,
    DeviceRole, DeviceType, Device, Interface, Connection
)
from .serializers import *

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomGroupViewSet(viewsets.ModelViewSet):
    queryset = CustomGroup.objects.all()
    serializer_class = CustomGroupSerializer

class VLANViewSet(viewsets.ModelViewSet):
    queryset = VLAN.objects.all()
    serializer_class = VLANSerializer

class VRFViewSet(viewsets.ModelViewSet):
    queryset = VRF.objects.all()
    serializer_class = VRFSerializer

class SubnetViewSet(viewsets.ModelViewSet):
    queryset = Subnet.objects.all()
    serializer_class = SubnetSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class DeviceRoleViewSet(viewsets.ModelViewSet):
    queryset = DeviceRole.objects.all()
    serializer_class = DeviceRoleSerializer

class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer

class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
