from rest_framework import permissions


class IsPaymentOwner(permissions.BasePermission):
    message = "Access Denied"
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True
        return obj.user == request.user