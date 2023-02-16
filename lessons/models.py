import datetime

from django.db import models

from authapp.models import User, Webinar, Group
from lessons import tasks
from notifications.models import Notification
from notifications.services import create_lesson_notifications
from profileapp.models import TeacherSubject, Subject
from settings.models import RateTeachers, DeadlineSettings, WeekDays

NULLABLE = {'blank': True, 'null': True}


class Schedule(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название', **NULLABLE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель', related_name='schedule_teacher',
                                limit_choices_to={'is_teacher': True})
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа', related_name='schedule_group',
                              **NULLABLE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет', **NULLABLE)
    weekday = models.ManyToManyField(WeekDays, verbose_name='Дни недели')
    is_completed = models.BooleanField(verbose_name='Завершенно', default=False)

    @property
    def students(self):
        return self.group.students.all()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class ScheduleSettings(models.Model):
    shedule = models.ForeignKey(Schedule, **NULLABLE, on_delete=models.CASCADE, verbose_name='Расписание')
    lesson_duration = models.PositiveSmallIntegerField(verbose_name='Длительность урока, мин', default=0)
    count = models.IntegerField(verbose_name='Кол-во уроков', **NULLABLE)
    near_lesson = models.DateTimeField(**NULLABLE, verbose_name='Ближайший урок')
    last_lesson = models.DateTimeField(**NULLABLE, verbose_name='Последний урок')

    def __str__(self) -> str:
        return f'{self.shedule}'

    def get_str_time(self):
        return f'{self.near_lesson} to {self.last_lesson}'


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
    lesson_number = models.IntegerField(verbose_name='Номер урока', **NULLABLE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель', related_name='lesson_teacher',
                                limit_choices_to={'is_teacher': True})
    # students = models.ManyToManyField(User, related_name='lesson_student', limit_choices_to={'is_student': True})
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа', related_name='lesson_group',
                              **NULLABLE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name='Расписание', **NULLABLE)
    topic = models.CharField(verbose_name='Тема урока', **NULLABLE, max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет', **NULLABLE)
    date = models.DateTimeField(verbose_name='Дата урока')
    transfer_date = models.DateTimeField(verbose_name='Дата переноса', **NULLABLE)
    transfer_comment = models.TextField(verbose_name='Комментарий к переносу или отмене урока', **NULLABLE)
    teacher_status = models.BooleanField(verbose_name='Статус учителя', default=False)
    teacher_entry_date = models.DateTimeField(verbose_name='Дата входа на урок учителя', **NULLABLE)
    student_status = models.BooleanField(verbose_name='Статус ученика', default=False)
    student_entry_date = models.DateTimeField(verbose_name='Дата входа на урок ученика', **NULLABLE)
    lesson_status = models.CharField(verbose_name='Статус урока', max_length=15, choices=LESSON_STATUS_CHOICES,
                                     default=SCHEDULED)
    deadline = models.DateTimeField(verbose_name='Сроки сдачи домашнего задания', **NULLABLE)
    student_evaluation = models.IntegerField(verbose_name='Оценка урока учеником', **NULLABLE)
    student_rate_comment = models.TextField(verbose_name='Комментарий студента к оценке урока', **NULLABLE)
    teacher_evaluation = models.IntegerField(verbose_name='Оценка урока учителем', **NULLABLE)
    teacher_rate_comment = models.TextField(verbose_name='Комментарий учителя к оценке урока', **NULLABLE)

    @property
    def students(self):
        if self.group:
            return self.group.students
        return []

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.pk}-{self.teacher}-{self.subject}'

    def save(self, *args, **kwargs):
        need_to_create_webinar = False
        if self.pk is None:
            need_to_create_webinar = True

        super(Lesson, self).save(*args, **kwargs)

        lesson_count = Lesson.objects.filter(teacher=self.teacher, subject=self.subject)
        if self.lesson_status == Lesson.SCHEDULED:
            if not lesson_count:
                lesson_count = 0
                self.lesson_number = lesson_count + 1
            else:
                self.lesson_number = lesson_count.count() + 1
            if self.subject:
                questions = Subject.objects.filter(name=self.subject.name).first()
                if not self.teacher_rate_comment:
                    self.teacher_rate_comment = questions.questions

        if self.lesson_status == Lesson.DONE:
            # payment_for_lesson(self)  #TODO
            count = DeadlineSettings.objects.filter(subject=self.subject).first()
            if self.schedule and not self.schedule.is_completed:
                schedule_settings = ScheduleSettings.objects.filter(shedule=self.schedule).order_by('-pk').first()
                if schedule_settings:
                    if self.date.date() == schedule_settings.last_lesson.date():
                        self.schedule.is_completed = True
                        self.schedule.save()
            if self.deadline:
                pass
            elif count:
                days = datetime.timedelta(days=count.day_count)
                deadline = self.date + days
                self.deadline = deadline

        # TODO: for refactoring
        if self.group:
            if self.lesson_status == Lesson.RESCHEDULED:
                create_lesson_notifications(lesson_status=self.lesson_status, students=self.group.students,
                                            teacher=self.teacher,
                                            teacher_status=self.teacher_status, date=self.transfer_date,
                                            lesson_id=self.pk)
            else:
                create_lesson_notifications(lesson_status=self.lesson_status, students=self.group.students,
                                            teacher=self.teacher,
                                            teacher_status=self.teacher_status, date=self.date, lesson_id=self.pk)

        if need_to_create_webinar:
            webinar = Webinar.objects.create(
                name=f'webinar#{self.pk}',
                start_date=self.date,
                lesson=self
            )
            # tasks.create_webinar_and_users_celery.delay(webinar.pk)


class Feedback(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)
    student_evaluation = models.IntegerField(verbose_name='Оценка урока учеником', **NULLABLE)
    student_rate_comment = models.TextField(verbose_name='Комментарий студента к оценке урока', **NULLABLE)
    teacher_evaluation = models.IntegerField(verbose_name='Оценка урока учителем', **NULLABLE)
    teacher_rate_comment = models.TextField(verbose_name='Комментарий учителя к оценке урока', **NULLABLE)


class TeacherWorkHours(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель',
                                limit_choices_to={'is_teacher': True})
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', **NULLABLE)

    class Meta:
        verbose_name = 'Рабочие часы учителя'
        verbose_name_plural = 'Рабочие часы учителя'


class TeacherWorkHoursSettings(models.Model):
    teacher_work_hours = models.ForeignKey(TeacherWorkHours, **NULLABLE, on_delete=models.CASCADE,
                                           verbose_name='Рабочие часы учителя')
    weekday = models.ForeignKey(WeekDays, on_delete=models.CASCADE, verbose_name='День недели', **NULLABLE)
    start_time = models.TimeField(verbose_name='Начало работы', **NULLABLE)
    end_time = models.TimeField(verbose_name='Конец работы', **NULLABLE)

    class Meta:
        verbose_name = 'Настройки рабочих часов учителя'
        verbose_name_plural = 'Настройки рабочих часов учителя'


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
    students = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_student', verbose_name='Ученик',**NULLABLE)
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


class ManagerRequestsRejectTeacher(models.Model):
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Менеджер', related_name='reject_manager',
                                **NULLABLE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ученик', related_name='reject_student')
    old_teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Старый учитель',
                                    related_name='reject_old_teacher')
    new_teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Новый учитель',
                                    related_name='reject_new_teacher', limit_choices_to={'is_teacher': True},
                                    **NULLABLE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий к отказу от ученика', **NULLABLE)
    is_resolved = models.BooleanField(verbose_name='Решен', default=False)

    class Meta:
        verbose_name = 'Запрос на изменение учителя у ученика'
        verbose_name_plural = 'Запросы на изменение учителя у ученика'
