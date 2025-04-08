def get_user_menu(user):
    return [
        {
            "label": "Инвентарь",
            "icon": "fas fa-server",
            "url": "",
            "visible": user.has_perm("inventory.view_device"),
            "children": [
                {"label": "Организации", "url": "/organizations/", "icon": "fas fa-sitemap", "visible": user.has_perm("inventory.view_organization")},
                {"label": "Здания", "url": "/buildings/", "icon": "fas fa-city", "visible": user.has_perm("inventory.view_building")},
                {"label": "Локации", "url": "/locations/", "icon": "fas fa-map-marker-alt", "visible": user.has_perm("inventory.view_location")},
                {"label": "Устройства", "url": "/devices/", "icon": "fas fa-microchip", "visible": user.has_perm("inventory.view_device")},
                {"label": "Интерфейсы", "url": "/interfaces/", "icon": "fas fa-plug", "visible": user.has_perm("inventory.view_interface")},
                {"label": "Соединения", "url": "/connections/", "icon": "fas fa-link", "visible": user.has_perm("inventory.view_connection")},
                {"label": "Роли устройств", "url": "/device_roles/", "icon": "fas fa-briefcase", "visible": user.has_perm("inventory.view_devicerole")},
                {"label": "Производители", "url": "/manufacturers/", "icon": "fas fa-industry", "visible": user.has_perm("inventory.view_manufacturer")},
                {"label": "Модели устройств", "url": "/device_types/", "icon": "fas fa-laptop", "visible": user.has_perm("inventory.view_devicetype")},
            ]
        },
        {
            "label": "IPAM",
            "icon": "fas fa-network-wired",
            "url": "",
            "visible": user.has_perm("ipam.view_subnet"),
            "children": [
                {"label": "Подсети", "url": "/subnets/", "icon": "fas fa-route", "visible": user.has_perm("ipam.view_subnet")},
                {"label": "VLAN", "url": "/vlans/", "icon": "fas fa-layer-group", "visible": user.has_perm("ipam.view_vlan")},
                {"label": "VRF", "url": "/vrfs/", "icon": "fas fa-random", "visible": user.has_perm("ipam.view_vrf")},
            ]
        },
        # {
        #     "label": "Мониторинг",
        #     "icon": "fas fa-heartbeat",
        #     "url": "/monitoring/",
        #     "visible": user.has_perm("monitoring.view_devicestatus"),
        #     "children": []
        # },
        # {
        #     "label": "Сканирование",
        #     "icon": "fas fa-satellite-dish",
        #     "url": "/scanning/",
        #     "visible": user.has_perm("scanning.view_scan"),
        #     "children": []
        # },
        # {
        #     "label": "Топология",
        #     "icon": "fas fa-project-diagram",
        #     "url": "/topology/",
        #     "visible": user.has_perm("topology.view_topology"),
        #     "children": []
        # },
        # {
        #     "label": "Логи",
        #     "icon": "fas fa-history",
        #     "url": "/logs/",
        #     "visible": user.has_perm("logs.view_changelog"),
        #     "children": []
        # },
        # {
        #     "label": "Дополнительно",
        #     "icon": "fas fa-tools",
        #     "url": "",
        #     "visible": user.has_perm("extras.view_customfield"),
        #     "children": [
        #         {"label": "Поля", "url": "/custom-fields/", "icon": "fas fa-sliders-h", "visible": user.has_perm("extras.view_customfield")},
        #         {"label": "Теги", "url": "/tags/", "icon": "fas fa-tags", "visible": user.has_perm("extras.view_tag")},
        #     ]
        # },
        {
            "label": "Пользователи",
            "icon": "fas fa-user-shield",
            "url": "",
            "visible": user.is_superuser or user.has_perm("users.view_user"),
            "children": [
                {
                    "label": "Пользователи",
                    "url": "/users/",
                    "icon": "fas fa-user",
                    "visible": user.has_perm("users.view_user")
                },
                {
                    "label": "Группы",
                    "url": "/groups/",
                    "icon": "fas fa-users",
                    "visible": user.is_superuser or user.has_perm("auth.view_group")
                },
            ]
        },
    ]

def menu_context(request):
    return {
        'menu': get_user_menu(request.user)
    }
