from django.db import models
from inventory.models import Device, Location
from simple_history.models import HistoricalRecords

class NetworkMap(models.Model):
    name = models.CharField("Название карты", max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Локация")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "карта сети"
        verbose_name_plural = "карты сетей"


class MapDevicePlacement(models.Model):
    network_map = models.ForeignKey(NetworkMap, on_delete=models.CASCADE, related_name="placements")
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        unique_together = ("network_map", "device")