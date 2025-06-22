from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from inventory.models import Device
from terminal.models import DeviceAccess
import socket

def connect_device(request, pk):
    device = get_object_or_404(Device, pk=pk)

    if request.method == "POST":
        ip = request.POST.get("ip")
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        port = request.POST.get("port", "23")

        try:
            port = int(port)
        except ValueError:
            messages.error(request, "Неверный порт.")
            return redirect("inventory:device_detail", pk=device.pk)

        try:
            with socket.create_connection((ip, port), timeout=3):
                pass
        except (socket.timeout, ConnectionRefusedError, OSError):
            messages.error(request, "Не удалось подключиться. Проверьте IP и порт.")
            return redirect("inventory:device_detail", pk=device.pk)

        device.access.delete() if hasattr(device, "access") else None

        DeviceAccess.objects.create(
            device=device,
            ip=ip,
            username=username,
            password=password,
            port=port,
        )

        messages.success(request, "Подключение успешно установлено.")
        return redirect("inventory:device_detail", pk=device.pk)

    messages.error(request, "Метод запроса не поддерживается.")
    return redirect("inventory:device_detail", pk=device.pk)


def disconnect_device(request, pk):
    if request.method == "POST":
        device = get_object_or_404(Device, pk=pk)
        DeviceAccess.objects.filter(device=device).delete()
    return redirect("inventory:device_detail", pk=pk)