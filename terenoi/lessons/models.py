import pytz
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from authapp.models import User, VoxiAccount
from authapp.services import add_voxiaccount
from lessons.services import current_date
from notifications.models import Notification
from profileapp.models import TeacherSubject, Subject

NULLABLE = {'blank': True, 'null': True}


class Lesson(models.Model):
    SCHEDULED = 'SCH'
    PROGRESS = 'PRG'
    DONE = 'DN'
    CANCEL = 'CNL'

    LESSON_STATUS_CHOICES = (
        (SCHEDULED, 'Урок назначен'),
        (PROGRESS, 'Урок идет'),
        (DONE, 'Урок проведен'),
        (CANCEL, 'Урок отменен')
    )
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель', related_name='lesson_teacher',
                                limit_choices_to={'is_teacher': True})
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ученик', related_name='lesson_student',
                                limit_choices_to={'is_student': True})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет', **NULLABLE)
    date = models.DateTimeField(verbose_name='Дата урока')
    teacher_status = models.BooleanField(verbose_name='Статус учителя', default=False)
    student_status = models.BooleanField(verbose_name='Статус ученика', default=False)
    lesson_status = models.CharField(verbose_name='Статус урока', max_length=3, choices=LESSON_STATUS_CHOICES,
                                     default=SCHEDULED)
    record = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.teacher}-{self.student}-{self.subject}'

    def save(self, *args, **kwargs):
        Notification.objects.create(to_user=self.student, lesson_date=self.date, type=Notification.LESSON_SCHEDULED)
        Notification.objects.create(to_user=self.teacher, lesson_date=self.date, type=Notification.LESSON_SCHEDULED)
        student = VoxiAccount.objects.filter(user=self.student).first()
        if student is None:
            username = f'Student-{self.student.pk}'
            add_voxiaccount(self.student, username, self.student.username)
        if self.student_status and self.teacher_status and self.lesson_status == Lesson.SCHEDULED:
            self.lesson_status = Lesson.PROGRESS

        super(Lesson, self).save()


class LessonMaterials(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    material = models.FileField(upload_to='materials-for-lesson/', verbose_name='Материалы к уроку', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Материал к уроку'
        verbose_name_plural = 'Материалы к уроку'


class LessonHomework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    homework = models.FileField(upload_to='homework-for-lesson/', verbose_name='Домашнее задание к уроку',
                                **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Домашнее задание к уроку'
        verbose_name_plural = 'Домашнее задание к уроку'
