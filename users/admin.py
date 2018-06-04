from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'user_type', 'username', 'email', 'first_name', 'last_name', 'is_staff')

    fieldsets = (
        (None, {'fields': ('user_type', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    )


admin.site.register(User, UserAdmin)