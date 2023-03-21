from pathlib import Path

from django.conf import settings
from django.db import models

from authapp.models import User

NULLABLE = {'blank': True, 'null': True}


class Language(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    short_name = models.CharField(verbose_name='Сокращение', max_length=10)

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        return self.name


class LevelLanguage(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Язык',
                                 related_name='level_language')
    name = models.CharField(verbose_name='Название', max_length=50)

    class Meta:
        verbose_name = 'Уровень языка'
        verbose_name_plural = 'Уровни языка'

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(verbose_name='Название раздела', max_length=50)
    description = models.TextField(verbose_name='Описание раздела', max_length=1000, **NULLABLE)
    parent_section = models.ForeignKey('self', on_delete=models.CASCADE,
                                       verbose_name='Родительский раздел', **NULLABLE)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        if self.parent_section:
            return f'{self.parent_section.name} {self.name}'
        return self.name


class Resource(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Язык',
                                 related_name='resource_language', **NULLABLE)
    level_language = models.ManyToManyField(LevelLanguage, verbose_name='Уровень языка', **NULLABLE)
    title = models.CharField(verbose_name='Название', max_length=250)
    description = models.TextField(verbose_name='Описание', max_length=1500)
    preview = models.ImageField(upload_to='resource_img/', verbose_name='Превью', **NULLABLE)
    link_video = models.CharField(verbose_name='Ссылка на видео', max_length=500, **NULLABLE)
    link_resource = models.CharField(verbose_name='Ссылка на ресурс', max_length=500, **NULLABLE)
    label_resource = models.CharField(verbose_name='Лейбл для ресурса', max_length=250, **NULLABLE)
    tags = models.JSONField(verbose_name='Теги', **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    is_advice = models.BooleanField(verbose_name='Является ли советом', default=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Раздел',
                                related_name='section_resource')

    class Meta:
        indexes = [models.Index(fields=['is_advice', ])]
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'

    def __str__(self):
        return self.title

    def get_preview(self):
        if self.user:
            return self.user.get_avatar()
        my_file = Path(f'{settings.MEDIA_ROOT}/{self.preview}')
        if my_file.is_file():
            return f'{settings.BACK_URL}{settings.MEDIA_URL}{self.preview}'
        return ''


class ResourceLikeList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name='Ресурс')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def save(self, *args, **kwargs):
        like = ResourceLikeList.objects.filter(resource=self.resource, user=self.user)
        if not like:
            super(ResourceLikeList, self).save(*args, **kwargs)


class ResourceFavoriteList(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name='Ресурс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def save(self, *args, **kwargs):
        favorite = ResourceFavoriteList.objects.filter(resource=self.resource, user=self.user)
        if not favorite:
            super(ResourceFavoriteList, self).save(*args, **kwargs)
