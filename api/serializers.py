from rest_framework import serializers
from users.models import User, CustomGroup
from ipam.models import VLAN, VRF, Subnet
from inventory.models import (
    Organization, Building, Location, Manufacturer,
    DeviceRole, DeviceType, Device, Interface, Connection
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]
        read_only_fields = ["id"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "role", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CustomGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGroup
        fields = "__all__"

class VLANSerializer(serializers.ModelSerializer):
    class Meta:
        model = VLAN
        fields = "__all__"

class VRFSerializer(serializers.ModelSerializer):
    class Meta:
        model = VRF
        fields = "__all__"

class SubnetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subnet
        fields = "__all__"

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"

class DeviceRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceRole
        fields = "__all__"

class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = "__all__"

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interface
        fields = "__all__"

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = "__all__"
