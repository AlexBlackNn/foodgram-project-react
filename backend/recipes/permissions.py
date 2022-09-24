from rest_framework import permissions


class IsAuthorOrAdministratorOrReadOnly(permissions.BasePermission):
    """Доступ только автору администратору или только читать."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_anonymous or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
        )
