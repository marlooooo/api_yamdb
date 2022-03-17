from rest_framework.permissions import BasePermission, SAFE_METHODS

from .utils import get_role_permission_level


class ModeratorOrReadOnly(BasePermission):
    """Доступ только от модератора и выше."""
    MIN_PERMISSION_CLASS = 1

    def has_object_permission(self, request, view, obj):
        return (
            get_role_permission_level(
                request.user) >= self.MIN_PERMISSION_CLASS
            or request.user.is_staff
            or request.user.is_superuser
        )

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or request.user.is_authenticated()
        )


class AdminOrReadOnly(ModeratorOrReadOnly):
    """Доступ только от админа и выше."""
    # Не уверен в том, что это будет работать правильно
    MIN_PERMISSION_CLASS = 2