from pathlib import Path

import pytz
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

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
    alfa_id = models.BigIntegerField(verbose_name='Номер пользователя из alfa/amo crm', **NULLABLE)
    is_recruiting = models.BooleanField(default=False, verbose_name='Набор открыт')
    is_pass_generation = models.BooleanField(default=False, verbose_name='Сгенерировать пароль')
    is_verified = models.BooleanField(default=False, verbose_name='Верефицирован')
    is_online = models.BooleanField(default=False, verbose_name='Онлайн')
    is_crm = models.BooleanField(default=False, verbose_name='Из alfa/amo crm')
    crm_data = models.TextField(**NULLABLE)

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
        super(User, self).save(*args, **kwargs)

    def create_participant(self, webinar, participant_data, role):
        participant = participant_data.get('participant')
        PruffmeAccount.objects.create(
            webinar=webinar,
            user=self,
            ext_id=participant.get('id'),
            hash=participant.get('hash'),
            webinar_hash=participant.get('webinarHash'),
            session=participant_data.get('session'),
            role=role
        )


class Group(models.Model):
    STATUS_OPEN = 'open'
    STATUS_LEARN = 'lear'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_OPEN, 'Идет набор'),
        (STATUS_LEARN, 'Обучается'),
        (STATUS_DONE, 'Завершена'),
    )

    CREATE_NORMAL = 'normal'
    CREATE_FAST = 'fast'

    CREATE_TYPE = (
        (CREATE_NORMAL, 'Обычное создание группы'),
        (CREATE_FAST, 'Быстрое создание группы'),
    )

    title = models.CharField(max_length=50, verbose_name='Название группы')
    description = models.TextField(verbose_name='Описание')
    english_level = models.CharField(max_length=50, choices=User.LEVEL_CHOICES, default=User.BEGINNER,
                                     verbose_name='Уровень английского')
    status = models.CharField(choices=STATUSES, default=STATUS_OPEN, max_length=15, verbose_name='Статус')
    create_status = models.CharField(choices=CREATE_TYPE, default=CREATE_NORMAL, max_length=25, verbose_name='Тип создания')

    alfa_id = models.BigIntegerField(verbose_name='Номер из alfa crm', **NULLABLE)

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ответственный преподаватель', **NULLABLE)

    students = models.ManyToManyField(User, verbose_name='Ученики', related_name='group_students')

    crm_data = models.TextField(**NULLABLE)

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __str__(self):
        return f'{self.title}'


class UserStudyLanguage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    language = models.ManyToManyField(StudyLanguage, verbose_name='Язык обучения')

    class Meta:
        verbose_name = 'Язык обучения пользователя'
        verbose_name_plural = 'Языки обучения пользователей'


class Webinar(models.Model):
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE, **NULLABLE)

    name = models.CharField(**NULLABLE, max_length=150, verbose_name='Автоматическое название')

    ext_id = models.IntegerField(**NULLABLE)
    hash = models.CharField(**NULLABLE, max_length=255, verbose_name='Хэш')
    login = models.CharField(**NULLABLE, max_length=255, verbose_name='Хэш')
    landing = models.CharField(**NULLABLE, max_length=255, verbose_name='Хэш')

    start_date = models.DateTimeField(**NULLABLE, verbose_name='Время и дата начала урока')

    def save_info(self, webinar_response):
        webinar_data = webinar_response.get('webinar')
        if webinar_data:
            self.ext_id = webinar_data.get('id')
            self.hash = webinar_data.get('hash')
            self.login = webinar_data.get('login')
            self.landing = webinar_data.get('landing')
            self.save()


class WebinarRecord(models.Model):
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, **NULLABLE)
    record = models.CharField(**NULLABLE, max_length=255)


class PruffmeAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    ext_id = models.IntegerField(**NULLABLE)
    hash = models.CharField(**NULLABLE, max_length=255)
    webinar_hash = models.CharField(**NULLABLE, max_length=255)
    name = models.CharField(**NULLABLE, max_length=255)
    session = models.CharField(**NULLABLE, max_length=255)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, **NULLABLE)
    role = models.CharField(**NULLABLE, max_length=255)
