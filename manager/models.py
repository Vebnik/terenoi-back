from django.db import models


# class Student(models.Model):

#   ACTIVE = 'ACT'
#   PAUSE = 'PAU'
#   ARCHIVE = 'ARC'
#   CANCEL = 'CAN'

#   STATUS_USER = [
#     (ACTIVE, 'Активный'),
#     (PAUSE, 'На паузе'),
#     (ARCHIVE, 'Архивный'),
#     (CANCEL, 'Отказ'),
#   ]

#   name = models.CharField(max_length=100)
#   group = models.CharField(max_length=100)
#   ab = models.CharField(max_length=100)
#   balance = models.IntegerField('balance')
#   status = models.CharField(default=ACTIVE, choices=STATUS_USER, max_length=3)