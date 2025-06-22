from django.db import models
from inventory.models import Device
from simple_history.models import HistoricalRecords

class DeviceAccess(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name="access")
    username = models.CharField(max_length=64, verbose_name="Имя пользователя")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    ip = models.GenericIPAddressField(verbose_name="IP-адрес для SSH")
    port = models.IntegerField(default=22, verbose_name="Порт")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "доступ к устройству"
        verbose_name_plural = "доступы к устройствам"

    def __str__(self):
        return f"{self.device.name} ({self.ip})"
