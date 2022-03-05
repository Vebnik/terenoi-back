import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.sessions.models import Session
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from authapp.models import User
from authapp.services import send_notifications
from lessons.services import current_date

NULLABLE = {'blank': True, 'null': True}


class Notification(models.Model):
    LESSON_SCHEDULED = 'LSN_SCH'
    LESSON_COMING_SOON = 'LSN_CMN'
    LESSON_PROGRESS = 'LSN_PRG'
    LESSON_DONE = 'LSN_DN'
    LESSON_REQUEST_RESCHEDULED = 'LSN_REQ_RESCH'
    LESSON_RESCHEDULED = 'LSN_RESCH'
    LESSON_REQUEST_CANCEL = 'LSN_REQ_CNL'
    LESSON_CANCEL = 'LSN_CNL'

    CHOICES_NOTIFICATIONS = (
        (LESSON_SCHEDULED, 'Урок назначен'),
        (LESSON_COMING_SOON, 'Урок скоро состоится'),
        (LESSON_PROGRESS, 'Урок идет'),
        (LESSON_DONE, 'Урок проведен'),
        (LESSON_REQUEST_RESCHEDULED, 'Запрос на перенос урока'),
        (LESSON_REQUEST_CANCEL, 'Запрос на отмену урока'),
        (LESSON_RESCHEDULED, 'Урок перенесен'),
        (LESSON_CANCEL, 'Урок отменен')
    )

    to_user = models.ForeignKey(User, verbose_name='Уведомлениe пользователя', on_delete=models.CASCADE)
    lesson_id = models.IntegerField(verbose_name='Номер урока', **NULLABLE)
    lesson_date = models.DateTimeField(verbose_name='Дата урока', **NULLABLE)
    type = models.CharField(max_length=20, choices=CHOICES_NOTIFICATIONS, verbose_name='Тип уведомления', **NULLABLE)
    message = models.CharField(max_length=255, verbose_name='Сообщение', **NULLABLE)
    is_read = models.BooleanField(default=False, verbose_name='Просмотрено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


class PaymentNotification(models.Model):
    PAID = 'PD'
    AWAITING_PAYMENT = 'AP'
    CHOICES_NOTIFICATIONS = (
        (PAID, 'Оплачено'),
        (AWAITING_PAYMENT, 'Ожидает оплаты')
    )

    to_user = models.ForeignKey(User, verbose_name='Уведомлениe пользователя', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(verbose_name='Дата оплаты', **NULLABLE)
    message = models.CharField(max_length=255, verbose_name='Сообщение', **NULLABLE)
    type = models.CharField(max_length=20, choices=CHOICES_NOTIFICATIONS, verbose_name='Тип уведомления', **NULLABLE)
    is_read = models.BooleanField(default=False, verbose_name='Просмотрено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Уведомление об оплате'
        verbose_name_plural = 'Уведомления об оплате'
