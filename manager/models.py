from django.db import models

from authapp.models import User


NULLABLE = {'blank': True, 'null': True}

class AdditionalUserNumber(models.Model):
  user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='User')
  phone = models.CharField(max_length=25, verbose_name='Дополнительный телефон', **NULLABLE)
  comment = models.TextField(verbose_name='Комментраий', **NULLABLE)