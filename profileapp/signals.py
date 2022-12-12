from django.db.models.signals import post_save
from django.dispatch import receiver
import finance
from authapp.models import User
from profileapp.models import ReferralPromo
from profileapp.services import generateRefPromo


@receiver(post_save, sender=User)
def create_ref_link(sender, instance, created, **kwargs):
    user_ref = ReferralPromo.objects.filter(user=instance).first()
    if not user_ref:
        promo = generateRefPromo()
        ReferralPromo.objects.create(user=instance, user_link=promo)
    if not instance.is_staff:
        if instance.is_student:
            user_balance = finance.models.StudentBalance.objects.filter(user=instance).first()
            if not user_balance:
                finance.models.StudentBalance.objects.create(user=instance)
        elif instance.is_teacher:
            user_balance = finance.models.TeacherBalance.objects.filter(user=instance).first()
            if not user_balance:
                finance.models.TeacherBalance.objects.create(user=instance)
