from django.db.models.signals import post_save
from django.dispatch import receiver

from authapp.models import User
from finance.models import TeacherBankData
from settings.models import UserCity


@receiver(post_save, sender=User)
def add_city(sender, instance, **kwargs):
    user_city = UserCity.objects.filter(user=instance).first()
    if not user_city:
        UserCity.objects.create(user=instance)
    if instance.is_teacher:
        bank = TeacherBankData.objects.filter(user=instance).first()
        if not bank:
            TeacherBankData.objects.create(user=instance)