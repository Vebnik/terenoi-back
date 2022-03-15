import datetime
import calendar

import pytz
from dateutil.rrule import rrule, DAILY, WEEKLY
from django.conf import settings
from django.db import models
from django.db.models import Sum

import finance
from authapp.models import User, VoxiAccount
from authapp.services import add_voxiaccount
from lessons.services import get_record, payment_for_lesson
from notifications.models import Notification
from notifications.services import create_lesson_notifications
from profileapp.models import TeacherSubject, Subject
from settings.models import RateTeachers, DeadlineSettings, WeekDays

NULLABLE = {'blank': True, 'null': True}


class Lesson(models.Model):
    SCHEDULED = 'SCH'
    REQUEST_RESCHEDULED = 'REQ_RESCH'
    RESCHEDULED = 'RESCH'
    PROGRESS = 'PRG'
    DONE = 'DN'
    REQUEST_CANCEL = 'REQ_CNL'
    CANCEL = 'CNL'

    LESSON_STATUS_CHOICES = (
        (SCHEDULED, 'Урок назначен'),
        (REQUEST_RESCHEDULED, 'Запрос на перенос урока'),
        (RESCHEDULED, 'Урок перенесен'),
        (PROGRESS, 'Урок идет'),
        (DONE, 'Урок проведен'),
        (REQUEST_CANCEL, 'Запрос на отмену урока'),
        (CANCEL, 'Урок отменен')
    )

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель', related_name='lesson_teacher',
                                limit_choices_to={'is_teacher': True})
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ученик', related_name='lesson_student',
                                limit_choices_to={'is_student': True})
    topic = models.CharField(verbose_name='Тема урока', **NULLABLE, max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет', **NULLABLE)
    date = models.DateTimeField(verbose_name='Дата урока')
    transfer_date = models.DateTimeField(verbose_name='Дата переноса', **NULLABLE)
    transfer_comment = models.TextField(verbose_name='Комментарий к переносу или отмене урока', **NULLABLE)
    teacher_status = models.BooleanField(verbose_name='Статус учителя', default=False)
    student_status = models.BooleanField(verbose_name='Статус ученика', default=False)
    lesson_status = models.CharField(verbose_name='Статус урока', max_length=15, choices=LESSON_STATUS_CHOICES,
                                     default=SCHEDULED)
    deadline = models.DateTimeField(verbose_name='Сроки сдачи домашнего задания', **NULLABLE)
    student_evaluation = models.IntegerField(verbose_name='Оценка урока учеником', **NULLABLE)
    student_rate_comment = models.TextField(verbose_name='Комментарий студента к оценке урока', **NULLABLE)
    teacher_evaluation = models.IntegerField(verbose_name='Оценка урока учителем', **NULLABLE)
    teacher_rate_comment = models.TextField(verbose_name='Комментарий учителя к оценке урока', **NULLABLE)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.pk}-{self.teacher}-{self.student}-{self.subject}'

    def save(self, *args, **kwargs):
        super(Lesson, self).save()
        student = VoxiAccount.objects.filter(user=self.student).first()
        if student is None:
            username = f'Student-{self.student.pk}'
            add_voxiaccount(self.student, username, self.student.username)
        if self.lesson_status == Lesson.SCHEDULED:
            create_lesson_notifications(lesson_status=self.lesson_status, student=self.student, teacher=self.teacher,
                                        teacher_status=self.teacher_status, date=self.date, lesson_id=self.pk)
            questions = Subject.objects.filter(name=self.subject.name).first()
            self.teacher_rate_comment = questions.questions
        if self.lesson_status == Lesson.REQUEST_CANCEL:
            create_lesson_notifications(lesson_status=self.lesson_status, student=self.student, teacher=self.teacher,
                                        teacher_status=self.teacher_status, date=self.date, lesson_id=self.pk)
        if self.lesson_status == Lesson.CANCEL:
            create_lesson_notifications(lesson_status=self.lesson_status, student=self.student, teacher=self.teacher,
                                        teacher_status=self.teacher_status, date=self.date, lesson_id=self.pk)
        if self.student_status and self.teacher_status and self.lesson_status == Lesson.SCHEDULED:
            self.lesson_status = Lesson.PROGRESS
            create_lesson_notifications(lesson_status=self.lesson_status, student=self.student, teacher=self.teacher,
                                        teacher_status=self.teacher_status, date=self.date, lesson_id=self.pk)
        if self.lesson_status == Lesson.REQUEST_RESCHEDULED:
            create_lesson_notifications(lesson_status=self.lesson_status, student=self.student, teacher=self.teacher,
                                        teacher_status=self.teacher_status, date=self.date, lesson_id=self.pk)
        if self.lesson_status == Lesson.RESCHEDULED:
            create_lesson_notifications(lesson_status=self.lesson_status, student=self.student, teacher=self.teacher,
                                        teacher_status=self.teacher_status, date=self.transfer_date, lesson_id=self.pk)
        if self.lesson_status == Lesson.DONE:
            get_record(lesson_id=self.pk, lesson_date=self.date)
            payment_for_lesson(self)
            count = DeadlineSettings.objects.filter(subject=self.subject).first()
            if count:
                days = datetime.timedelta(days=count.day_count)
                deadline = self.date + days
                self.deadline = deadline
        super(Lesson, self).save()


class LessonMaterials(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    material = models.FileField(upload_to='materials-for-lesson/', verbose_name='Материалы к уроку', **NULLABLE)
    text_material = models.TextField(**NULLABLE, verbose_name='Текстовое поле для материалов и комментариев')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Материал к уроку'
        verbose_name_plural = 'Материалы к уроку'


class LessonHomework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    homework = models.FileField(upload_to='homework-for-lesson/', verbose_name='Домашнее задание к уроку',
                                **NULLABLE)
    text_homework = models.TextField(**NULLABLE, verbose_name='Текстовое домашнее задание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Домашнее задание к уроку'
        verbose_name_plural = 'Домашнее задание к уроку'


class LessonRateHomework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    rate = models.IntegerField(verbose_name='Оценка домашнего задания', **NULLABLE)
    rate_comment = models.TextField(**NULLABLE, verbose_name='Комментарий к домашнему заданию')

    class Meta:
        verbose_name = 'Оценки домашнего задания ученика'
        verbose_name_plural = 'Оценки домашнего задания'


class VoximplantRecordLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    session_id = models.BigIntegerField(verbose_name='Айди сессии звонка')
    record = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Данные звонка'
        verbose_name_plural = 'Данные звонка'


class ManagerRequests(models.Model):
    REQUEST_RESCHEDULED = 'REQ_RESCH'
    RESCHEDULED = 'RESCH'
    REQUEST_CANCEL = 'REQ_CNL'
    CANCEL = 'CNL'
    REJECT = 'REJ'

    REQUEST_CHOICES = (
        (REQUEST_RESCHEDULED, 'Запрос на перенос урока'),
        (RESCHEDULED, 'Урок перенесен'),
        (REQUEST_CANCEL, 'Запрос на отмену урока'),
        (CANCEL, 'Урок отменен'),
        (REJECT, 'Запрос отклонен'),
    )

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Менеджер', related_name='lesson_manager',
                                **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='lesson_user')
    type = models.CharField(verbose_name='Тип запроса', choices=REQUEST_CHOICES, max_length=15, **NULLABLE)
    date = models.DateTimeField(verbose_name='Дата урока', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий к переносу или отмене урока', **NULLABLE)
    is_resolved = models.BooleanField(verbose_name='Решен', default=False)

    class Meta:
        verbose_name = 'Запрос для изменения урока'
        verbose_name_plural = 'Запросы для изменения уроков'


class Schedule(models.Model):
    title = models.CharField(max_length=50, **NULLABLE, verbose_name='Название')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель', related_name='schedule_teacher',
                                limit_choices_to={'is_teacher': True})
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ученик', related_name='schedule_student',
                                limit_choices_to={'is_student': True})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет', **NULLABLE)
    weekday = models.ManyToManyField(WeekDays, verbose_name='Дни недели')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class ScheduleSettings(models.Model):
    shedule = models.ForeignKey(Schedule, **NULLABLE, on_delete=models.CASCADE, verbose_name='Расписание')
    count = models.IntegerField(verbose_name='Кол-во уроков', **NULLABLE)
    near_lesson = models.DateTimeField(**NULLABLE, verbose_name='Ближайший урок')
    last_lesson = models.DateTimeField(**NULLABLE, verbose_name='Последний урок')

    def save(self, *args, **kwargs):
        super(ScheduleSettings, self).save(*args, **kwargs)
        lesson = Lesson.objects.filter(student=self.shedule.student, teacher=self.shedule.teacher,
                                       date=self.near_lesson)
        if lesson:
            super(ScheduleSettings, self).save(*args, **kwargs)
        else:
            number_list = []
            for i in self.shedule.weekday.all().values('number'):
                number_list.append(i['number'])
            date_list = rrule(freq=WEEKLY, dtstart=self.near_lesson, count=self.count,
                              wkst=calendar.firstweekday(),
                              byweekday=number_list)

            len_date_list = len(list(date_list))
            for i, date in enumerate(list(date_list)):
                Lesson.objects.create(student=self.shedule.student, teacher=self.shedule.teacher,
                                      subject=self.shedule.subject, date=date)
                if i == len_date_list - 1:
                    self.last_lesson = date

        super(ScheduleSettings, self).save(*args, **kwargs)
