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
                                limit_choices_to={'is_teacher': True})
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ученик', related_name='lesson_student',
                                limit_choices_to={'is_student': True})
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
            username = f'Student-{self.student.pk}'
            add_voxiaccount(self.student, username, self.student.first_name)

        if self.student_status and self.teacher_status:
            self.lesson_status = Lesson.PROGRESS
        super(Lesson, self).save()
