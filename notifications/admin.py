from django.contrib import admin
from notifications.models import Notification, PaymentNotification, ManagerNotification, HomeworkNotification, \
    LessonRateNotification, CourseNotification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'is_read', 'created_at')


@admin.register(PaymentNotification)
class PaymentNotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'is_read', 'created_at')


@admin.register(ManagerNotification)
class ManagerNotificationAdmin(admin.ModelAdmin):
    list_display = ('manager', 'type', 'to_user', 'lesson_id', 'is_read', 'created_at')


@admin.register(HomeworkNotification)
class HomeworkNotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'type', 'is_read', 'created_at')


@admin.register(LessonRateNotification)
class LessonRateNotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'type', 'is_read', 'created_at')


@admin.register(CourseNotification)
class CourseNotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user','course', 'type', 'is_read', 'created_at')