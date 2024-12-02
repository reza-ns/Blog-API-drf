from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_superuser", "is_staff")


UserAdmin.fieldsets [2][1]['fields'] =(
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "groups",
                    "user_permissions",
                )


admin.site.register(User, CustomUserAdmin)