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

    def get_minutes(self):
        minutes = (self.time_duration.hour * 60) + self.time_duration.minute
        return minutes

    def get_materials(self):
        my_file = Path(f'{settings.MEDIA_ROOT}/{self.materials}')
        if my_file.is_file():
            return f'{settings.BACK_URL}{settings.MEDIA_URL}{self.materials}'
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

    def get_minutes(self):
        minutes = (self.time_duration.hour * 60) + self.time_duration.minute
        return minutes

    def get_materials(self):
        my_file = Path(f'{settings.MEDIA_ROOT}/{self.materials}')
        if my_file.is_file():
            return f'{settings.BACK_URL}{settings.MEDIA_URL}{self.materials}'
        return ''


class CourseWishList(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Вишлист'
        verbose_name_plural = 'Вишлист'

    def save(self, *args, **kwargs):
        wish = CourseWishList.objects.filter(course=self.course, user=self.user)
        if not wish:
            super(CourseWishList, self).save(*args, **kwargs)


class CourseLikeList(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def save(self, *args, **kwargs):
        wish = CourseLikeList.objects.filter(course=self.course, user=self.user)
        if not wish:
            super(CourseLikeList, self).save(*args, **kwargs)


class PurchasedCourses(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Купленный курс'
        verbose_name_plural = 'Купленные курсы'


class PurchasedCoursesRequest(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='Курс')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Менеджер', related_name='course_manager',
                                **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='course_user')
    is_resolved = models.BooleanField(verbose_name='Решен', default=False)

    class Meta:
        verbose_name = 'Запрос на покупку курса'
        verbose_name_plural = 'Запросы на покупку курсов'
