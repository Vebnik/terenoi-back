from django.db import models

# Create your models here.
from authapp.models import User

NULLABLE = {'blank': True, 'null': True}


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название предмета', **NULLABLE)
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
            print(user_subjects.values('subject'))
            for sub in user_subjects.values('subject'):
                if sub['subject'] == self.subject.pk:
                    TeacherSubject.objects.get(subject=self.subject).delete()
            super(TeacherSubject, self).save(*args, **kwargs)
