from django.shortcuts import render
from NetScope.common.context_processors import get_user_menu
from inventory import models as inv
from ipam import models as ipam
from users.models import User
from topology.models import NetworkMap


def home_dashboard(request):
    user = request.user

    def safe_count(model, perm):
        return model.objects.count() if user.has_perm(perm) else None

    counts = {
        "organization": safe_count(inv.Organization, "inventory.view_organization"),
        "building": safe_count(inv.Building, "inventory.view_building"),
        "location": safe_count(inv.Location, "inventory.view_location"),
        "device": safe_count(inv.Device, "inventory.view_device"),
        "interface": safe_count(inv.Interface, "inventory.view_interface"),
        "connection": safe_count(inv.Connection, "inventory.view_connection"),
        "devicerole": safe_count(inv.DeviceRole, "inventory.view_devicerole"),
        "manufacturer": safe_count(inv.Manufacturer, "inventory.view_manufacturer"),
        "devicetype": safe_count(inv.DeviceType, "inventory.view_devicetype"),
        "roleicon": safe_count(inv.RoleIcon, "inventory.view_roleicon"),
        "subnet": safe_count(ipam.Subnet, "ipam.view_subnet"),
        "vlan": safe_count(ipam.VLAN, "ipam.view_vlan"),
        "vrf": safe_count(ipam.VRF, "ipam.view_vrf"),
        "user": safe_count(User, "users.view_user"),
        "group": safe_count(User.groups.rel.model, "auth.view_group"),
        "passwordresetrequest": None,  
        "networkmap": safe_count(NetworkMap, "topology.view_networkmap"),
    }

    return render(request, "home.html", {
        "menu": get_user_menu(user),
        "counts": counts,
    })
