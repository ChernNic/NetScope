from django.db import models
from simple_history.models import HistoricalRecords

class VLAN(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя VLAN")
    vid = models.PositiveIntegerField(verbose_name="VLAN ID", unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "VLAN"
        verbose_name_plural = "VLANы"

    def __str__(self):
        return f"{self.name}"


class VRF(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя VRF", unique=True)
    rd = models.CharField(max_length=50, verbose_name="Route Distinguisher", unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "VRF"
        verbose_name_plural = "VRF"

    def __str__(self):
        return self.name


class Subnet(models.Model):
    prefix = models.CharField(max_length=43, verbose_name="Подсеть (CIDR)", unique=True)  # Например, 192.168.0.0/24
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    vlan = models.ForeignKey(VLAN, on_delete=models.SET_NULL, null=True, blank=True, related_name="subnets", verbose_name="VLAN")
    vrf = models.ForeignKey(VRF, on_delete=models.SET_NULL, null=True, blank=True, related_name="subnets", verbose_name="VRF")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "подсеть"
        verbose_name_plural = "подсети"

    def __str__(self):
        return self.prefix
