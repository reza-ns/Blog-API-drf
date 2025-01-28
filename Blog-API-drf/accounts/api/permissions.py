from rest_framework import permissions
from accounts.models import User

class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.role == User.UserRole.SUPERUSER:
            return True
        return request.user.is_authenticated and request.user == obj