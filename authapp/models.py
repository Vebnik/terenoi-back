from pathlib import Path

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz

from authapp.services import add_voxiaccount

NULLABLE = {'blank': True, 'null': True}


class StudyLanguage(models.Model):
    name = models.CharField(verbose_name='Язык обучения', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Язык обучения'
        verbose_name_plural = 'Языки обучения'

    def __str__(self):
        return self.name


class User(AbstractUser):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский')
    )

    BEGINNER = "Beginner"
    ELEMENTARY = "Elementary"
    PRE_INTERMEDIATE = "Pre-intermediate"
    INTERMEDIATE = "Intermediate"
    UPPER_INTERMEDIATE = "Upper-intermediate"
    ADVANCED = "Advanced"

    LEVEL_CHOICES = (
        (BEGINNER, 'Beginner'),
        (ELEMENTARY, 'Elementary'),
        (PRE_INTERMEDIATE, 'Pre-intermediate'),
        (INTERMEDIATE, 'Intermediate'),
        (UPPER_INTERMEDIATE, 'Upper-intermediate'),
        (ADVANCED, 'Advanced'),
    )

    avatar = models.ImageField(upload_to='user_avatar/', verbose_name='Avatar', **NULLABLE)
    birth_date = models.DateField(verbose_name='Дата Рождения', **NULLABLE)
    phone = models.CharField(max_length=25, verbose_name='Телефон', **NULLABLE)
    telegram = models.CharField(max_length=255, verbose_name='Telegram', **NULLABLE)
    whatsapp = models.CharField(max_length=255, verbose_name='Whatsapp', **NULLABLE)
    bio = models.TextField(verbose_name='О себе', **NULLABLE)
    gender = models.TextField(max_length=10, choices=GENDER_CHOICES, **NULLABLE, verbose_name='Пол')
    time_zone = models.CharField(max_length=32, choices=TIMEZONES, default='Asia/Almaty', verbose_name='Часовой пояс')
    is_student = models.BooleanField(default=True, verbose_name='Ученик')
    is_teacher = models.BooleanField(default=False, verbose_name='Учитель')
    education = models.CharField(max_length=255, verbose_name='Образование', **NULLABLE)
    experience = models.TextField(verbose_name='Опыт работы', **NULLABLE)
    english_level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default=BEGINNER,
                                     verbose_name='Уровень английского у ученика')
    student_class = models.CharField(max_length=50, verbose_name='Класс ученика', **NULLABLE)
    alfa_id = models.BigIntegerField(verbose_name='Номер пользователя из alfa/amo crm',**NULLABLE)
    is_recruiting = models.BooleanField(default=False, verbose_name='Набор открыт')
    is_pass_generation = models.BooleanField(default=False, verbose_name='Сгенерировать пароль')
    is_verified = models.BooleanField(default=False, verbose_name='Верефицирован')
    is_online = models.BooleanField(default=False, verbose_name='Онлайн')
    is_crm = models.BooleanField(default=False, verbose_name='Из alfa/amo crm')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_avatar(self):
        my_file = Path(f'{settings.MEDIA_ROOT}/{self.avatar}')
        if my_file.is_file():
            return f'{settings.BACK_URL}{settings.MEDIA_URL}{self.avatar}'
        return ''

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if 'pbkdf2_sha256' not in self.password:
            password = make_password(self.password)
            self.password = password
        if self.is_teacher:
            voxi_user = VoxiAccount.objects.filter(user=self).first()
            if voxi_user is None:
                username = f'Teacher-{self.pk}'
                add_voxiaccount(self, username, self.username)
        super(User, self).save(*args, **kwargs)


class UserStudyLanguage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    language = models.ManyToManyField(StudyLanguage, verbose_name='Язык обучения')

    class Meta:
        verbose_name = 'Язык обучения пользователя'
        verbose_name_plural = 'Языки обучения пользователей'


class VoxiAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    voxi_user_id = models.CharField(max_length=15, **NULLABLE, verbose_name='id пользователя Voxiplant')
    voxi_username = models.CharField(max_length=150, unique=True, verbose_name='Логин Voxiplant')
    voxi_display_name = models.CharField(max_length=150, verbose_name='Имя Voxiplant')
    voxi_password = models.CharField(max_length=50, verbose_name='Пароль Voxiplant')

    class Meta:
        verbose_name = 'Voxiplant Аккаунт'
        verbose_name_plural = 'Voxiplant Аккаунты'
