import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models

from authapp.services import add_voxiaccount

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    avatar = models.TextField(verbose_name='Аватар', **NULLABLE)
    birth_date = models.DateField(verbose_name='День Рождения', **NULLABLE)
    phone = models.CharField(max_length=25, verbose_name='Телефон', **NULLABLE)
    bio = models.TextField(verbose_name='О себе', **NULLABLE)
    is_student = models.BooleanField(default=False, verbose_name='Ученик')
    is_teacher = models.BooleanField(default=False, verbose_name='Учитель')
    education = models.CharField(max_length=255, verbose_name='Образование', **NULLABLE)
    experience = models.TextField(verbose_name='Опыт работы', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Верефицирован')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        print(self.is_teacher)
        if self.is_teacher:
            self.is_staff = True
            voxi_user = VoxiAccount.objects.filter(user=self).first()
            if voxi_user is None:
                username = f'teacher{self.pk}'
                add_voxiaccount(self, username, self.first_name)
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
