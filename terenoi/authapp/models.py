from django.contrib.auth.models import AbstractUser
from django.db import models

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
