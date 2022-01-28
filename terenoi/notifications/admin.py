from django.contrib import admin
from notifications.models import Notification


@admin.register(Notification)
class UserAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'is_read', 'created_at')
