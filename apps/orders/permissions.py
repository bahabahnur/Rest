from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_customer

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return (
                request.user and request.user.is_authenticated
                and request.user == obj.customer
                and request.user.is_customer and obj.customer.is_customer
                )
