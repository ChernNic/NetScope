import os
from django.db import models
from simple_history.models import HistoricalRecords
from django.core.exceptions import ObjectDoesNotExist
from django.templatetags.static import static

from NetScope import settings

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
        try:
            return f"{self.name} ({self.organization.name})"
        except (ObjectDoesNotExist, AttributeError):
            return self.name


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
        try:
            return f"{self.name} ({self.building.name})"
        except (ObjectDoesNotExist, AttributeError):
            return self.name


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

    @property
    def auto_icon_path(self):
        """
        Ищет иконку в static/icons/roles/ по названию роли.
        Поддерживает: .svg, .eps, .png, .webp
        """
        search_dir = os.path.join(settings.BASE_DIR, "static", "icons", "roles")
        normalized_name = self.name.lower().replace(" ", "_")

        if not os.path.isdir(search_dir):
            return None

        for file in os.listdir(search_dir):
            filename, ext = os.path.splitext(file)
            if ext.lower() in [".svg", ".eps", ".png", ".webp"]:
                fname = filename.lower()
                if fname == normalized_name or fname.startswith(normalized_name) or normalized_name in fname:
                    return f"/static/icons/roles/{file}"
        return None

    @property
    def icon_url(self) -> str | None:
        """
        1) Если к роли привязали иконку через RoleIcon — используем её.
        2) Иначе пробуем найти файл автоматически по названию (auto_icon_path).
        """
        if self.assigned_icons.exists():
            icon = self.assigned_icons.first()
            return static(f"icons/roles/{icon.file_name}")
        return self.auto_icon_path
    
    
class RoleIcon(models.Model):
    file_name = models.CharField(max_length=255, unique=True, verbose_name="Файл иконки", null=True)
    roles = models.ManyToManyField("DeviceRole", related_name="assigned_icons", verbose_name="Назначенные роли")

    class Meta:
        verbose_name = "иконка роли"
        verbose_name_plural = "иконки ролей"

    @property
    def file_url(self):
        return f"/static/icons/roles/{self.file_name}"

    def __str__(self):
        return self.file_name



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
    
    @property
    def icon_url(self):
        """Возвращает URL иконки, привязанной к роли устройства."""
        if self.role and self.role.assigned_icons.exists():
            icon = self.role.assigned_icons.first()
            return static(f"icons/roles/{icon.file_name}")
        return None

    def __str__(self):
        try:
            return f"{self.name} ({self.device_type.name})"
        except (ObjectDoesNotExist, AttributeError):
            return self.name


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
        try:
            return f"{self.name} ({self.device.name})"
        except (ObjectDoesNotExist, AttributeError):
            return self.name


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
        try:
            return f"{self.interface1.name} <-> {self.interface2.name}"
        except (ObjectDoesNotExist, AttributeError):
            return "неполное соединение"
