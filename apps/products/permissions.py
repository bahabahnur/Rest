from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    CRUD владельцу пользователя к его продуктам
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_owner

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return (
                request.user and request.user.is_authenticated
                and request.user == obj.author
                and request.user.is_owner and obj.author.is_owner
                )
