from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("id", "username", "email", "phone_number", "is_active")
    list_filter = ("role",)
    readonly_fields = ("last_login",)

    fieldsets = (
        (None, {'fields': ("username", "email", "phone_number", "password", "last_login")}),
        ('Permissions', {'fields': ("is_active", "role")})
    )

    add_fieldsets = (
        (None, {'fields': ("username", "email", "phone_number", "role", "password1", "password2")}),
    )

    search_fields = ("email", "phone_number")
    ordering = ("date_joined",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
