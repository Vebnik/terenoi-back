from django.db import models


class Section(models.Model):
    name = models.CharField(verbose_name='Название раздела', max_length=50)
    description = models.TextField(verbose_name='Описание раздела', max_length=1000)
    section = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Раздел')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
