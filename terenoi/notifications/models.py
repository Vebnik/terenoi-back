from django.db import models

# Create your models here.
from authapp.models import User

NULLABLE = {'blank': True, 'null': True}


class Notification(models.Model):
    to_user = models.ForeignKey(User, verbose_name='Уведомлениe пользователя', on_delete=models.CASCADE)
    message = models.CharField(max_length=255, verbose_name='Сообщение', **NULLABLE)
    is_read = models.BooleanField(default=False, verbose_name='Просмотрено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
