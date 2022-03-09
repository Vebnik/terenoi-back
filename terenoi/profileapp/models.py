from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import finance
from authapp.models import User
from profileapp.services import generateRefPromo

NULLABLE = {'blank': True, 'null': True}


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название предмета', **NULLABLE)
    questions = models.TextField(verbose_name='Вопросы к предмету', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return f'{self.name}'


class TeacherSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель',
                             limit_choices_to={'is_teacher': True})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')

    class Meta:
        verbose_name = 'Предметы учителей'
        verbose_name_plural = 'Предметы учителей'

    def __str__(self):
        return f'{self.subject}'

    def save(self, *args, **kwargs):
        user_subjects = TeacherSubject.objects.filter(user=self.user).select_related()
        if len(user_subjects) == 0:
            super(TeacherSubject, self).save(*args, **kwargs)
        else:
            for sub in user_subjects.values('subject'):
                if sub['subject'] == self.subject.pk:
                    TeacherSubject.objects.get(subject=self.subject).delete()
            super(TeacherSubject, self).save(*args, **kwargs)


class ReferralPromo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user')
    user_link = models.CharField(max_length=10, verbose_name='Реферальный промо пользователя', unique=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', verbose_name='Друг',
                                  null=True)
    from_user_link = models.CharField(max_length=10, verbose_name='Реферальный промо друга', **NULLABLE)
    friend_is_used = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Реферальная программа'
        verbose_name_plural = 'Реферальная программа'


class ManagerToUser(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджр', related_name='terenoi_manger')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='terenoi_user')

    class Meta:
        verbose_name = 'Менеджер-Пользователь'
        verbose_name_plural = 'Менеджер-Пользователь'


class UserParents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',
                             limit_choices_to={'is_student': True})
    full_name = models.CharField(verbose_name='ФИО Родителя', max_length=255)
    parent_phone = models.CharField(max_length=25, verbose_name='Телефон родителя', **NULLABLE)
    parent_email = models.CharField(max_length=100, verbose_name='Email родителя', **NULLABLE)

    class Meta:
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'


class GlobalUserPurpose(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',
                             limit_choices_to={'is_student': True})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    purpose = models.CharField(max_length=255, verbose_name='Цель')

    class Meta:
        verbose_name = 'Цель ученика'
        verbose_name_plural = 'Цели учеников'


class LanguageInterface(models.Model):
    RUSSIAN = 'RU'
    KAZAKH = 'KZ'
    ENGLISH = 'EN'
    LANGUAGE_INTERFACE_CHOICES = (
        (RUSSIAN, 'Русский'),
        (KAZAKH, 'Казахстанский'),
        (ENGLISH, 'Английский'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    interface_language = models.CharField(max_length=10, choices=LANGUAGE_INTERFACE_CHOICES, default=RUSSIAN,
                                          verbose_name='Язык интерфейса')

    class Meta:
        verbose_name = 'Язык интерфейса пользователя'
        verbose_name_plural = 'Языки интерфейса пользователя'


class Interests(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        interest = Interests.objects.filter(name=self.name)
        if not interest:
            super(Interests, self).save(*args, **kwargs)
        else:
            Interests.objects.get(name=self.name).delete()
            super(Interests, self).save(*args, **kwargs)


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    interests = models.ManyToManyField(Interests)

    class Meta:
        verbose_name = 'Интерес пользователя'
        verbose_name_plural = 'Интересы пользователей'
