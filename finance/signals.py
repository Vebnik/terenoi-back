import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from finance.models import StudentBalance, HistoryPaymentStudent, HistoryPaymentTeacher
from profileapp.models import ReferralPromo
from settings.models import ReferralSettings


@receiver(post_save, sender=HistoryPaymentStudent)
def ref_bonus_student(sender, instance, **kwargs):
    user = instance.student
    ref_promo = ReferralPromo.objects.filter(user=user).first()
    friend_lesson_count = ReferralSettings.objects.all().first().friend_lesson_count
    friend_amount = ReferralSettings.objects.all().first().friend_amount
    if ref_promo.is_used and not ref_promo.friend_is_used:
        ref_promo.friend_is_used = True
        ref_promo.save()
        HistoryPaymentStudent.objects.create(student=user,
                                                 payment_date=datetime.datetime.now(),
                                                 lesson_count=friend_lesson_count, referral=True)


@receiver(post_save, sender=HistoryPaymentTeacher)
def ref_bonus_teacher(sender, instance, **kwargs):
    user = instance.teacher
    ref_promo = ReferralPromo.objects.filter(user=user).first()
    friend_lesson_count = ReferralSettings.objects.all().first().friend_lesson_count
    friend_amount = ReferralSettings.objects.all().first().friend_amount
    if ref_promo.is_used and not ref_promo.friend_is_used:
        ref_promo.friend_is_used = True
        ref_promo.save()
        HistoryPaymentTeacher.objects.create(teacher=user,
                                                 payment_date=datetime.datetime.now(),
                                                 amount=friend_amount, referral=True, is_enrollment=True)