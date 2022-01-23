import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models

from authapp.services import add_voxiaccount

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    STUDENT = 'ST'
    TEACHER = 'TH'
    MANAGER = 'MN'

    ROLE_CHOICES = (
        (STUDENT, 'Студент'),
        (TEACHER, 'Учитель'),
        (MANAGER, 'Менеджер'),
    )

    avatar = models.TextField(verbose_name='Аватар', **NULLABLE)
    birth_date = models.DateField(verbose_name='День Рождения', **NULLABLE)
    phone = models.CharField(max_length=25, verbose_name='Телефон', **NULLABLE)
    bio = models.TextField(verbose_name='О себе', **NULLABLE)
    role = models.CharField(verbose_name='Роль', max_length=2, choices=ROLE_CHOICES, default=STUDENT)
    education = models.CharField(max_length=255, verbose_name='Образование', **NULLABLE)
    experience = models.TextField(verbose_name='Опыт работы', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Верефицирован')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if self.role == User.TEACHER:
            voxi_user = VoxiAccount.objects.filter(user=self).first()
            if voxi_user is None:
                add_voxiaccount(self, self.username, self.first_name)
        super(User, self).save(*args, **kwargs)


class VoxiAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    voxi_user_id = models.CharField(max_length=15, **NULLABLE, verbose_name='id пользователя Voxiplant')
    voxi_username = models.CharField(max_length=150, unique=True, verbose_name='Логин Voxiplant')
    voxi_display_name = models.CharField(max_length=150, verbose_name='Имя Voxiplant')
    voxi_password = models.CharField(max_length=50, verbose_name='Пароль Voxiplant')

    class Meta:
        verbose_name = 'Voxiplant Аккаунт'
        verbose_name_plural = 'Voxiplant Аккаунты'
