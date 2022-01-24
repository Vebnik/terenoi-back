from django.db import models

# Create your models here.
from authapp.models import User


class Subject(models.Model):
    ENGLISH = 'EN'
    GERMAN = 'GRM'
    HISTORY = 'HS'

    SUBJECT_CHOICES = (
        (ENGLISH, 'Английский'),
        (GERMAN, 'Немецкий'),
        (HISTORY, 'История'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель', limit_choices_to={'is_teacher': True})
    subject = models.CharField(verbose_name='Предмет', max_length=3, choices=SUBJECT_CHOICES)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def save(self, *args, **kwargs):
        user_subjects = Subject.objects.filter(user=self.user).select_related()
        if len(user_subjects) == 0:
            super(Subject, self).save(*args, **kwargs)
        else:
            for sub in user_subjects.values('subject'):
                if sub['subject'] == self.subject:
                    Subject.objects.get(subject=self.subject).delete()
            super(Subject, self).save(*args, **kwargs)
