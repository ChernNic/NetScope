from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import DetailView
from django.templatetags.static import static
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q

from inventory.models import Interface, Connection
from .models import MapDevicePlacement, NetworkMap
from inventory.models import Device, Connection, Interface


class NetworkMapDetailView(DetailView):
    model = NetworkMap
    template_name = "topology/networkmap_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        network_map = self.object

        # Все устройства в локации
        all_devices = Device.objects.filter(location=network_map.location)

        # Все соединения
        connections = Connection.objects.select_related("interface1__device", "interface2__device").filter(
            interface1__device__location=network_map.location,
            interface2__device__location=network_map.location
        )

        connected_devices = set()
        edges = []

        # Подсчёт количества соединений между каждой парой устройств
        connection_counts = {}

        for conn in connections:
            dev_a = conn.interface1.device
            dev_b = conn.interface2.device
            connected_devices.update([dev_a.id, dev_b.id])

            key = tuple(sorted((dev_a.id, dev_b.id)))
            connection_counts[key] = connection_counts.get(key, 0) + 1
            count = connection_counts[key] - 1

            if count == 0:
                smooth = False
            else:
                smooth = {
                    "enabled": True,
                    "type": "curvedCW" if count % 2 == 0 else "curvedCCW",
                    "roundness": 0.2 + count * 0.05
                }

            edges.append({
                "id": conn.id,
                "from": dev_a.id,
                "to": dev_b.id,
                "label": f"{conn.interface1.name} ({conn.interface1.ip_address}) ↔ {conn.interface2.name} ({conn.interface2.ip_address})",
                "color": {"color": "#00cc66"},
                "smooth": smooth
            })

        # Все устройства, которые размещены на холсте
        placed_ids = set(
            MapDevicePlacement.objects.filter(network_map=network_map).values_list("device_id", flat=True)
        )
        added_device_ids = connected_devices.union(placed_ids)

        # Узлы
        nodes = []
        for dev in all_devices:
            if dev.id not in added_device_ids:
                continue
            icon_url = dev.icon_url if hasattr(dev, "icon_url") and dev.icon_url else static("icons/default.png")
            nodes.append({
                "id": dev.id,
                "label": f"{dev.name}\n{dev.device_type.name if dev.device_type else ''}",
                "title": f"<b>{dev.name}</b><br>{dev.device_type.name if dev.device_type else ''}",
                "shape": "image",
                "image": icon_url,
                "size": 40
            })

        context["nodes_json"] = json.dumps(nodes, cls=DjangoJSONEncoder)
        context["edges_json"] = json.dumps(edges, cls=DjangoJSONEncoder)
        context["available_devices"] = all_devices  # Показываем все
        context["added_device_ids"] = list(added_device_ids)

        placements = {
            p.device_id: {"x": p.x, "y": p.y}
            for p in MapDevicePlacement.objects.filter(network_map=network_map)
        }
        context["device_positions"] = json.dumps(placements)

        return context




def available_interfaces(request):
    device_id = request.GET.get("device_id")
    if not device_id:
        return JsonResponse([], safe=False)

    interfaces = Interface.objects.filter(device_id=device_id).filter(
        connections1__isnull=True,
        connections2__isnull=True
    ).values("id", "name")

    return JsonResponse(list(interfaces), safe=False)


@csrf_exempt
@require_POST
def create_connection(request):
    try:
        data = json.loads(request.body)
        intf1 = Interface.objects.get(id=data["interface1"])
        intf2 = Interface.objects.get(id=data["interface2"])

        if Connection.objects.filter(interface1=intf1).exists() or Connection.objects.filter(interface2=intf1).exists():
            return HttpResponseBadRequest("Интерфейс 1 уже используется")
        if Connection.objects.filter(interface1=intf2).exists() or Connection.objects.filter(interface2=intf2).exists():
            return HttpResponseBadRequest("Интерфейс 2 уже используется")

        Connection.objects.create(interface1=intf1, interface2=intf2)
        return JsonResponse({"ok": True})

    except (KeyError, Interface.DoesNotExist, json.JSONDecodeError):
        return HttpResponseBadRequest("Невалидные данные")
    

@csrf_exempt
@require_POST
def delete_connection_by_id(request):
    conn_id = request.GET.get("id")
    if not conn_id:
        return JsonResponse({"error": "Missing connection ID"}, status=400)

    try:
        conn = Connection.objects.get(id=conn_id)
        conn.delete()
        return JsonResponse({"ok": True})
    except Connection.DoesNotExist:
        return JsonResponse({"error": "Connection not found"}, status=404)



@csrf_exempt
@require_POST
def save_device_position(request, map_id):
    try:
        data = json.loads(request.body)
        device = Device.objects.get(id=data["device_id"])
        placement, _ = MapDevicePlacement.objects.update_or_create(
            network_map_id=map_id,
            device=device,
            defaults={"x": data["x"], "y": data["y"]}
        )
        return JsonResponse({"ok": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_POST
def remove_device_from_map(request, map_id):
    try:
        data = json.loads(request.body)
        MapDevicePlacement.objects.filter(network_map_id=map_id, device_id=data["device_id"]).delete()
        return JsonResponse({"ok": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
