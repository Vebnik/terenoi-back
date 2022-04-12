import datetime
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver
from authapp.services import send_notifications
from lessons.models import Lesson
from lessons.services import current_date
from notifications.models import Notification, PaymentNotification, HomeworkNotification, LessonRateNotification


@receiver(post_save, sender=Notification)
def notifications_handler(sender, instance, **kwargs):
    if not instance.is_read:
        lesson_date = current_date(instance.to_user, instance.lesson_date)
        if instance.to_user.is_online:
            channel_layer = get_channel_layer()
            created_at = current_date(instance.to_user, instance.created_at)
            data = {"user": instance.to_user.username, "lesson_id": instance.lesson_id, "created_at": created_at,
                    "lesson_date": lesson_date,
                    "type": instance.type, "is_read": instance.is_read}
            async_to_sync(channel_layer.group_send)(
                f'{instance.to_user.username}_group', {
                    'type': 'send_notification',
                    'value': json.dumps(data, cls=DjangoJSONEncoder)
                }
            )
        else:
            lesson = Lesson.objects.filter(pk=instance.lesson_id).first()
            if instance.type == Notification.LESSON_SCHEDULED:
                subject = 'Урок назначен'
                body = f'Урок назначен на '
                send_notifications(instance.to_user, subject, body, lesson_date)
            elif instance.type == Notification.LESSON_COMING_SOON:
                subject = 'Урок скоро состоится'
                body = f'Урок состоится в '
                send_notifications(instance.to_user, subject, body, lesson_date)
            elif instance.type == Notification.LESSON_PROGRESS:
                subject = 'Урок начинается'
                body = f'Урок начнется  в '
                send_notifications(instance.to_user, subject, body, lesson_date)
            elif instance.type == Notification.LESSON_CANCEL:
                subject = 'Урок отменен'
                body = f'Урок отменен '
                send_notifications(instance.to_user, subject, body, lesson_date)
            elif instance.type == Notification.LESSON_REQUEST_RESCHEDULED:
                if instance.to_user.is_teacher:
                    subject = 'Запрос на перенос урока'
                    body = f'Ученик {lesson.student.first_name} {lesson.student.last_name} хочет перенести урок {lesson.lesson_number}'
                    send_notifications(instance.to_user, subject, body)
            elif instance.type == Notification.LESSON_RESCHEDULED:
                subject = 'Урок перенесен'
                body = f'Урок перенесен'
                send_notifications(instance.to_user, subject, body)
            elif instance.type == Notification.LESSON_REQUEST_CANCEL:
                if instance.to_user.is_teacher:
                    subject = 'Запрос на отмену урока'
                    body = f'Ученик {lesson.student.first_name} {lesson.student.last_name} хочет отменить урок {lesson.lesson_number}'
                    send_notifications(instance.to_user, subject, body)


@receiver(post_save, sender=PaymentNotification)
def payment_notifications_handler(sender, instance, **kwargs):
    if not instance.is_read:
        if instance.payment_date:
            payment_date = current_date(instance.to_user, instance.payment_date)
        else:
            payment_date = current_date(instance.to_user, datetime.datetime.now())
        if instance.to_user.is_online:
            channel_layer = get_channel_layer()
            created_at = current_date(instance.to_user, instance.created_at)
            data = {"user": instance.to_user.username, "created_at": created_at,
                    "payment_date": payment_date,
                    "type": instance.type, "is_read": instance.is_read}
            async_to_sync(channel_layer.group_send)(
                f'{instance.to_user.username}_group', {
                    'type': 'send_notification',
                    'value': json.dumps(data, cls=DjangoJSONEncoder)
                }
            )
        else:
            pass


@receiver(post_save, sender=HomeworkNotification)
def homework_notifications_handler(sender, instance, **kwargs):
    if not instance.is_read:
        lesson = Lesson.objects.filter(pk=instance.lesson_id).first()
        if instance.to_user.is_online:
            channel_layer = get_channel_layer()
            created_at = current_date(instance.to_user, instance.created_at)
            data = {"user": instance.to_user.username, "created_at": created_at,
                    "type": instance.type, "is_read": instance.is_read}
            async_to_sync(channel_layer.group_send)(
                f'{instance.to_user.username}_group', {
                    'type': 'send_notification',
                    'value': json.dumps(data, cls=DjangoJSONEncoder)
                }
            )
        else:
            if instance.type == HomeworkNotification.HOMEWORK_ADD:
                subject = 'Домашнее задание добавлено'
                body = f'Домашнее задание добавлено'
                send_notifications(instance.to_user, subject, body)
            elif instance.type == HomeworkNotification.HOMEWORK_CHECK:
                subject = 'Домашнее задание проверено'
                body = f'Домашнее задание проверено'
                send_notifications(instance.to_user, subject, body)


@receiver(post_save, sender=LessonRateNotification)
def homework_notifications_handler(sender, instance, **kwargs):
    if not instance.is_read:
        lesson = Lesson.objects.filter(pk=instance.lesson_id).first()
        if instance.to_user.is_online:
            channel_layer = get_channel_layer()
            created_at = current_date(instance.to_user, instance.created_at)
            data = {"user": instance.to_user.username, "created_at": created_at,
                    "type": instance.type, "is_read": instance.is_read}
            async_to_sync(channel_layer.group_send)(
                f'{instance.to_user.username}_group', {
                    'type': 'send_notification',
                    'value': json.dumps(data, cls=DjangoJSONEncoder)
                }
            )
        else:
            pass
