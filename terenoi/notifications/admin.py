from django.contrib import admin
from notifications.models import Notification, PaymentNotification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'is_read', 'created_at')


@admin.register(PaymentNotification)
class PaymentNotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'is_read', 'created_at')
