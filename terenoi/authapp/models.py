from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz
from authapp.services import add_voxiaccount


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский')
    )
    RUSSIAN = 'RU'
    KAZAKH = 'KZ'
    ENGLISH = 'EN'
    LANGUAGE_CHOICES = (
        (RUSSIAN, 'Русский'),
        (KAZAKH, 'Казахстанский'),
        (ENGLISH, 'Английский'),
    )

    avatar = models.ImageField(upload_to='user_avatar/', verbose_name='Avatar', **NULLABLE)
    birth_date = models.DateField(verbose_name='Дата Рождения', **NULLABLE)
    phone = models.CharField(max_length=25, verbose_name='Телефон', **NULLABLE)
    bio = models.TextField(verbose_name='О себе', **NULLABLE)
    gender = models.TextField(max_length=10, choices=GENDER_CHOICES, **NULLABLE, verbose_name='Пол')
    time_zone = models.CharField(max_length=32, choices=TIMEZONES, default='Asia/Almaty', verbose_name='Часовой пояс')
    is_student = models.BooleanField(default=True, verbose_name='Ученик')
    is_teacher = models.BooleanField(default=False, verbose_name='Учитель')
    education = models.CharField(max_length=255, verbose_name='Образование', **NULLABLE)
    experience = models.TextField(verbose_name='Опыт работы', **NULLABLE)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, verbose_name='Язык обучения', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Верефицирован')
    is_online = models.BooleanField(default=False, verbose_name='Онлайн')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

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


class VoxiAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    voxi_user_id = models.CharField(max_length=15, **NULLABLE, verbose_name='id пользователя Voxiplant')
    voxi_username = models.CharField(max_length=150, unique=True, verbose_name='Логин Voxiplant')
    voxi_display_name = models.CharField(max_length=150, verbose_name='Имя Voxiplant')
    voxi_password = models.CharField(max_length=50, verbose_name='Пароль Voxiplant')

    class Meta:
        verbose_name = 'Voxiplant Аккаунт'
        verbose_name_plural = 'Voxiplant Аккаунты'

