def get_user_menu(user):
    def make_item(label, key, url, icon, permission):
        return {
            "label": label,
            "key": key,
            "url": url,
            "icon": icon,
            "permission": permission,
            "visible": user.has_perm(permission)
        }

    def section(label, icon, children):
        visible_items = [item for item in children if item["visible"]]
        return {
            "label": label,
            "icon": icon,
            "visible": bool(visible_items),
            "children": visible_items
        }

    inventory_items = [
        make_item("Организации", "organization", "/organizations/", "fas fa-sitemap", "inventory.view_organization"),
        make_item("Здания", "building", "/buildings/", "fas fa-city", "inventory.view_building"),
        make_item("Локации", "location", "/locations/", "fas fa-map-marker-alt", "inventory.view_location"),
        make_item("Устройства", "device", "/devices/", "fas fa-microchip", "inventory.view_device"),
        make_item("Интерфейсы", "interface", "/interfaces/", "fas fa-plug", "inventory.view_interface"),
        make_item("Соединения", "connection", "/connections/", "fas fa-link", "inventory.view_connection"),
        make_item("Роли устройств", "devicerole", "/device_roles/", "fas fa-briefcase", "inventory.view_devicerole"),
        make_item("Производители", "manufacturer", "/manufacturers/", "fas fa-industry", "inventory.view_manufacturer"),
        make_item("Модели устройств", "devicetype", "/device_types/", "fas fa-laptop", "inventory.view_devicetype"),
        make_item("Иконки ролей", "roleicon", "/role_icons/", "fas fa-icons", "inventory.view_roleicon"),
    ]

    ipam_items = [
        make_item("Подсети", "subnet", "/subnets/", "fas fa-route", "ipam.view_subnet"),
        make_item("VLAN", "vlan", "/vlans/", "fas fa-layer-group", "ipam.view_vlan"),
        make_item("VRF", "vrf", "/vrfs/", "fas fa-random", "ipam.view_vrf"),
    ]

    users_items = [
        make_item("Пользователи", "user", "/users/", "fas fa-user", "users.view_user"),
        make_item("Группы", "group", "/groups/", "fas fa-users", "auth.view_group") if user.is_superuser else None,
        make_item("Заявки на смену пароля", "passwordresetrequest", "/resetrequests/", "fas fa-key", "users.view_passwordresetrequest") if user.is_superuser else None,
    ]
    users_items = [i for i in users_items if i]

    topology_items = [
        make_item("Карты сетей", "networkmap", "/maps/", "fas fa-map", "topology.view_networkmap"),
    ]

    return [
        section("Топология", "fas fa-project-diagram", topology_items),
        section("Инвентарь", "fas fa-server", inventory_items),
        section("IPAM", "fas fa-network-wired", ipam_items),
        section("Пользователи", "fas fa-user-shield", users_items),
    ]

def menu_context(request):
    return {
        'menu': get_user_menu(request.user)
    }
