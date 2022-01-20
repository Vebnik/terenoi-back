from django.contrib import admin
from authapp.models import User, VoxiAccount


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'last_login', 'role')
    list_filter = ('is_staff', 'is_active')


@admin.register(VoxiAccount)
class VoxiAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'voxi_username', 'voxi_display_name')

