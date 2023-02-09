from django.db import models
from pathlib import Path
from authapp.models import User
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Courses(models.Model):
    img = models.ImageField(upload_to='course_img/', verbose_name='Превью курса', **NULLABLE)
    title = models.CharField(verbose_name='Название курса', max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    time_duration = models.TimeField(verbose_name='Длительность курса')
    description = models.TextField(verbose_name='Описание курса')
    materials = models.FileField(upload_to='materials-for-courses/', verbose_name='Полезные материалы к курсу',
                                 **NULLABLE)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

    def get_course_img(self):
        my_file = Path(f'{settings.MEDIA_ROOT}/{self.img}')
        if my_file.is_file():
            return f'{settings.BACK_URL}{settings.MEDIA_URL}{self.img}'
        return ''


class LessonCourse(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='Курс')
    img = models.ImageField(upload_to='course_lesson_img/', verbose_name='Превью урока', **NULLABLE)
    title = models.CharField(verbose_name='Название урока', max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    time_duration = models.TimeField(verbose_name='Длительность урока')
    description = models.TextField(verbose_name='Описание урока')
    video = models.FileField(upload_to='video-for-lesson/', verbose_name='Видео урока')
    materials = models.FileField(upload_to='materials-for-lesson/', verbose_name='Полезные материалы к уроку',
                                 **NULLABLE)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title

    def get_lesson_img(self):
        my_file = Path(f'{settings.MEDIA_ROOT}/{self.img}')
        if my_file.is_file():
            return f'{settings.BACK_URL}{settings.MEDIA_URL}{self.img}'
        return ''

    def get_video(self):
        my_file = Path(f'{settings.MEDIA_ROOT}/{self.video}')
        if my_file.is_file():
            return f'{settings.BACK_URL}{settings.MEDIA_URL}{self.video}'
        return ''
