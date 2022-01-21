from django.db import models

from authapp.models import User, VoxiAccount
from authapp.services import add_voxiaccount


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
                                limit_choices_to={'role': User.TEACHER})
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ученик', related_name='lesson_student',
                                limit_choices_to={'role': User.STUDENT})
    date = models.DateTimeField(verbose_name='Дата урока')
    teacher_status = models.BooleanField(verbose_name='Статус учителя', default=False)
    student_status = models.BooleanField(verbose_name='Статус ученика', default=False)
    lesson_status = models.CharField(verbose_name='Статус урока', max_length=3, choices=LESSON_STATUS_CHOICES,
                                     default=SCHEDULED)
    record = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def save(self, *args, **kwargs):
        student = VoxiAccount.objects.filter(user=self.student).first()
        if student is None:
            add_voxiaccount(self, self.student.username, self.student.first_name)
        super(Lesson, self).save()
