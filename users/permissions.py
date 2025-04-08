from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """ Разрешает полный доступ администраторам, остальным только чтение """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    """ Разрешает доступ владельцу объекта или администратору """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

class CustomRolePermission(permissions.BasePermission):
    """ Универсальные права доступа на основе ролей """
    def has_permission(self, request, view):
        required_role = getattr(view, 'required_role', None)
        if required_role is None:
            return True  # Если у вью не указана роль, разрешаем доступ
        return hasattr(request.user, 'role') and request.user.role == required_role
