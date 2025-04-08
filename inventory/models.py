from django.db import models
from simple_history.models import HistoricalRecords

class Organization(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название организации")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    history = HistoricalRecords(verbose_name="История")

    class Meta:
        verbose_name = "организация"
        verbose_name_plural = "организации"

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название здания")
    organization = models.ForeignKey(
        Organization, related_name="buildings", on_delete=models.CASCADE, verbose_name="Организация"
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    history = HistoricalRecords(verbose_name="История")

    class Meta:
        verbose_name = "здание"
        verbose_name_plural = "здания"

    def __str__(self):
        return f"{self.name} ({self.organization.name})"


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Местоположение")
    building = models.ForeignKey(
        Building, related_name="locations", on_delete=models.CASCADE, verbose_name="Здание"
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    history = HistoricalRecords(verbose_name="История")

    class Meta:
        verbose_name = "локация"
        verbose_name_plural = "локации"

    def __str__(self):
        return f"{self.name} ({self.building.name})"


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Производитель")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    history = HistoricalRecords(verbose_name="История")

    class Meta:
        verbose_name = "производитель"
        verbose_name_plural = "производители"

    def __str__(self):
        return self.name


class DeviceRole(models.Model):
    name = models.CharField(max_length=100, verbose_name="Роль устройства")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    history = HistoricalRecords(verbose_name="История")

    class Meta:
        verbose_name = "роль устройства"
        verbose_name_plural = "роли устройств"

    def __str__(self):
        return self.name


class DeviceType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Модель устройства")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    history = HistoricalRecords(verbose_name="История")

    class Meta:
        verbose_name = "модель устройства"
        verbose_name_plural = "модели устройств"

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название устройства")
    device_type = models.ForeignKey(
        DeviceType, related_name="devices", on_delete=models.CASCADE, verbose_name="Модель устройства"
    )
    manufacturer = models.ForeignKey(
        Manufacturer, related_name="devices", on_delete=models.CASCADE, verbose_name="Производитель"
    )
    role = models.ForeignKey(
        DeviceRole, related_name="devices", on_delete=models.CASCADE, verbose_name="Роль устройства"
    )
    location = models.ForeignKey(
        Location, related_name="devices", on_delete=models.CASCADE, verbose_name="Локация"
    )
    status = models.CharField(max_length=50, verbose_name="Статус", default="Active")

    history = HistoricalRecords(verbose_name="История")

    class Meta:
        verbose_name = "устройство"
        verbose_name_plural = "устройства"

    def __str__(self):
        return f"{self.name} ({self.device_type.name})"


class Interface(models.Model):
    device = models.ForeignKey(
        Device, related_name="interfaces", on_delete=models.CASCADE, verbose_name="Устройство"
    )
    name = models.CharField(max_length=100, verbose_name="Название интерфейса")
    ip_address = models.GenericIPAddressField(verbose_name="IP-адрес", blank=True, null=True)

    history = HistoricalRecords(verbose_name="История")

    class Meta:
        verbose_name = "интерфейс"
        verbose_name_plural = "интерфейсы"

    def __str__(self):
        return f"{self.name} ({self.device.name})"


class Connection(models.Model):
    interface1 = models.ForeignKey(
        Interface, related_name="connections1", on_delete=models.CASCADE, verbose_name="Интерфейс 1"
    )
    interface2 = models.ForeignKey(
        Interface, related_name="connections2", on_delete=models.CASCADE, verbose_name="Интерфейс 2"
    )

    history = HistoricalRecords(verbose_name="История")

    class Meta:
        verbose_name = "соединение"
        verbose_name_plural = "соединения"

    def __str__(self):
        return f"{self.interface1.name} <-> {self.interface2.name}"
