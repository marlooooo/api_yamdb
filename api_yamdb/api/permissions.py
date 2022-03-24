from rest_framework.permissions import BasePermission, SAFE_METHODS


class OwnerOrReadOnly(BasePermission):
    """Доступ только от автора и выше."""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return (
            obj.author == request.user
            or request.user.permission_level() >= 1
            or request.user.is_staff
            or request.user.is_superuser
        )


class AdminOrReadOnly(BasePermission):
    """Доступ только от админа и выше."""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            (request.user.is_authenticated and
             (request.user.is_staff or request.user.permission_level() == 2 or
              request.user.is_superuser)
             )
        )


class UserViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_staff or
                request.user.is_superuser or
                request.user.permission_level() == 2
            )
        )


class CustomIsAuthorized(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.permission_level()
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
