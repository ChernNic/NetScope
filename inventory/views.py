import json
import os
from pathlib import Path

from django.conf import settings
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from inventory.models import Device, RoleIcon, DeviceRole
from extras.scaffold.views import AutoDetailView


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name="dispatch")
class RoleIconListView(View):
    """
    Отображает все файлы из /static/icons/roles/** в виде списка.
    Позволяет:
      • Привязывать к иконке одну или несколько DeviceRole (AJAX‑POST).
      • Добавлять новую иконку (модальное окно + multipart POST).
    """
    template_name = "inventory/roleicon_list.html"
    icons_dir: Path = Path(settings.BASE_DIR, "static", "icons", "roles")

    # ---------- helpers ----------------------------------------------------
    @staticmethod
    def _sync_fs_with_db(icons_dir: Path) -> None:
        """
        Убедимся, что в БД есть записи RoleIcon для всех файлов в директории.
        Не удаляет записи, если файл был убран с диска — это позволит
        «мягко» обрабатывать устаревшие иконки.
        """
        if not icons_dir.exists():
            icons_dir.mkdir(parents=True, exist_ok=True)

        fs_filenames = {p.name for p in icons_dir.iterdir() if p.is_file()}
        db_filenames = set(RoleIcon.objects.values_list("file_name", flat=True))

        new_files = fs_filenames - db_filenames
        RoleIcon.objects.bulk_create([RoleIcon(file_name=f) for f in new_files])

    @staticmethod
    def _unassigned_roles() -> list[DeviceRole]:
        """
        Роли, ещё не прикреплённые ни к одной иконке.
        """
        return DeviceRole.objects.exclude(
            id__in=RoleIcon.roles.through.objects.values_list("devicerole_id", flat=True)
        )

    # ---------- http methods ----------------------------------------------
    def get(self, request):
        self._sync_fs_with_db(self.icons_dir)

        icons_qs = (
            RoleIcon.objects
            .prefetch_related(
                Prefetch("roles", queryset=DeviceRole.objects.order_by("name"))
            )
            .order_by("file_name")
        )
        context = {
            "icons": icons_qs,
            "available_roles": self._unassigned_roles(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        ct = request.content_type or ""
        # ─── JSON‑действия (attach / remove / delete icon) ────────────────
        if ct.startswith("application/json"):
            try:
                data     = json.loads(request.body.decode())
                icon_id  = int(data.get("icon_id"))
            except (json.JSONDecodeError, ValueError, TypeError):
                return HttpResponseBadRequest("Невалидный JSON")

            icon = get_object_or_404(RoleIcon, pk=icon_id)

            # --- удалить саму иконку + запись --------------------------------
            if data.get("delete_icon"):
                # стираем файл с диска (если ещё есть)
                try:
                    os.remove(self.icons_dir / icon.file_name)
                except FileNotFoundError:
                    pass
                icon.delete()
                return JsonResponse({"ok": True})

            # --- открепить / прикрепить роль --------------------------------
            role_id = int(data.get("role_id", 0))
            role    = get_object_or_404(DeviceRole, pk=role_id)

            if data.get("remove"):
                icon.roles.remove(role)
                return JsonResponse({"ok": True, "role_id": role.id, "role_name": role.name})

            icon.roles.add(role)
            badge_html = (
                f'<span class="badge badge-outline flex items-center gap-1" '
                f'data-role-id="{role.id}">'
                f'{role.name}'
                f'<i class="fa-solid fa-xmark text-xs cursor-pointer remove-role-btn" '
                f'data-icon-id="{icon.id}" data-role-id="{role.id}"></i></span>'
            )
            return JsonResponse({"ok": True, "role_id": role.id, "role_badge_html": badge_html})

        # ─── multipart: загрузка новой иконки ──────────────────────────────
        upload = request.FILES.get("file")
        if upload:
            if upload.size > 1_000_000:
                return HttpResponseBadRequest("Файл > 1 MB")

            ext = Path(upload.name).suffix.lower()
            if ext not in {".png", ".svg", ".webp", ".eps"}:
                return HttpResponseBadRequest("Недопустимый формат")

            dst_path = self.icons_dir / Path(upload.name).name
            counter  = 1
            while dst_path.exists():
                dst_path = self.icons_dir / f"{dst_path.stem}_{counter}{ext}"
                counter += 1

            with dst_path.open("wb+") as fh:
                for chunk in upload.chunks():
                    fh.write(chunk)

            self._sync_fs_with_db(self.icons_dir)
            return JsonResponse({"ok": True})

        return HttpResponseBadRequest("Неизвестный формат запроса")
    

class DeviceDetailView(AutoDetailView):
    model = Device
    context_object_name = "object"

    def get_extra_tabs(self):
        return [
            {
                "id": "tab-console",
                "label": "Консоль",
                "template": "inventory/partials/console_tab.html"
            },
            {
                "id": "tab-interfaces",
                "label": "Интерфейсы",
                "template": "inventory/partials/interfaces_tab.html"
            },
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.get_object()

        context["extra_tabs"] = self.get_extra_tabs()

        if hasattr(device, "access"):
            context["terminal_ws_url"] = f"/ws/terminal/{device.id}/"

        context["interfaces"] = device.interfaces.all()
        return context



from django.views.generic import DetailView
from inventory.models import Device

class EmptyView(DetailView):
    model = Device
    template_name = "empty.html"