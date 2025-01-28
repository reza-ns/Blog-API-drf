from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.role == User.UserRole.SUPERUSER:
            return True
        return request.user.is_authenticated and request.user.role == User.UserRole.AUTHOR


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.role == User.UserRole.SUPERUSER:
            return True
        return bool(obj.user == request.user)


class IsSubscriberOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.role == User.UserRole.SUPERUSER:
            return True
        elif obj.is_paid:
            if request.user.is_authenticated and request.user.role == User.UserRole.SUBSCRIBER:
                return True
            elif obj.user == request.user:
                return True
        else:
            return True
