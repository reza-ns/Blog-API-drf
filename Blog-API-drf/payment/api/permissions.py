from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class IsPaymentOwner(permissions.BasePermission):
    message = "Access Denied"
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.role == User.UserRole.SUPERUSER:
            return True
        return obj.user == request.user