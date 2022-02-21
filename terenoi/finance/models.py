import datetime
from django.db import models
from authapp.models import User
from lessons.models import Lesson
from profileapp.models import Subject, ReferralPromo
from settings.models import ReferralSettings

NULLABLE = {'blank': True, 'null': True}

TENGE = 'KZT'
DOLLARS = 'USD'
CURRENCY_CHOICES = (
    (TENGE, 'KZT'),
    (DOLLARS, 'USD')
)


class StudentBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ученик',
                             limit_choices_to={'is_student': True})
    money_balance = models.IntegerField(verbose_name='Баланс', **NULLABLE)
    currency = models.CharField(verbose_name='Валюта', choices=CURRENCY_CHOICES, default=TENGE, max_length=5)
    lessons_balance = models.IntegerField(verbose_name='Баланс уроков', **NULLABLE)
    bonus_lessons_balance = models.IntegerField(verbose_name='Бонусный баланс уроков', **NULLABLE)

    class Meta:
        verbose_name = 'Баланс ученика'
        verbose_name_plural = 'Баланс ученика'


class TeacherBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель',
                             limit_choices_to={'is_teacher': True})
    money_balance = models.IntegerField(verbose_name='Баланс', **NULLABLE)
    currency = models.CharField(verbose_name='Валюта', choices=CURRENCY_CHOICES, default=TENGE, max_length=5)
    bonus_money_balance = models.IntegerField(verbose_name='Бонусный баланс', **NULLABLE)
    withdrawal_money = models.IntegerField(verbose_name='Выведенные деньги', **NULLABLE)

    class Meta:
        verbose_name = 'Баланс учителя'
        verbose_name_plural = 'Баланс учителя'


class HistoryPaymentStudent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student', verbose_name='Ученик',
                                limit_choices_to={'is_student': True})
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager', verbose_name='Менеджер',
                                limit_choices_to={'is_staff': True}, **NULLABLE)
    payment_date = models.DateTimeField(verbose_name='Дата и время зачисления')
    amount = models.IntegerField(verbose_name='Сумма зачисления', **NULLABLE)
    currency = models.CharField(verbose_name='Валюта', choices=CURRENCY_CHOICES, default=TENGE, max_length=5)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет', **NULLABLE)
    lesson_count = models.IntegerField(verbose_name='Кол-во уроков', **NULLABLE)
    referral = models.BooleanField(verbose_name='Реферальная программа', default=False)

    class Meta:
        verbose_name = 'История операций ученика'
        verbose_name_plural = 'История операций ученика'

    def save(self, *args, **kwargs):
        student_balance = StudentBalance.objects.filter(user=self.student).first()
        if not self.referral:
            if not student_balance.money_balance:
                student_balance.money_balance = self.amount
                ref_user = ReferralPromo.objects.filter(user=self.student).first()
                lesson_count = ReferralSettings.objects.all().first().lesson_count
                amount = ReferralSettings.objects.all().first().amount
                if ref_user.from_user and not ref_user.is_used:
                    if ref_user.from_user.is_student:
                        HistoryPaymentStudent.objects.create(student=ref_user.from_user,
                                                             payment_date=datetime.datetime.now(),
                                                             lesson_count=lesson_count, referral=True)
                        ref_user.is_used = True
                        ref_user.save()
                    elif ref_user.from_user.is_teacher:
                        HistoryPaymentTeacher.objects.create(teacher=ref_user.from_user,
                                                             payment_date=datetime.datetime.now(),
                                                             amount=amount, referral=True)
                        ref_user.is_used = True
                        ref_user.save()
                elif ref_user.from_user_link and not ref_user.is_used:
                    link = ref_user.from_user_link
                    user = ReferralPromo.objects.filter(user_link=link).first().user
                    if user.is_student:
                        HistoryPaymentStudent.objects.create(student=user, payment_date=datetime.datetime.now(),
                                                             lesson_count=lesson_count, referral=True)
                        ref_user.is_used = True
                        ref_user.save()
                    elif user.is_teacher:
                        HistoryPaymentTeacher.objects.create(teacher=user, payment_date=datetime.datetime.now(),
                                                             amount=amount,
                                                             referral=True)
                        ref_user.is_used = True
                        ref_user.save()
            else:
                student_balance.money_balance += self.amount
            if not student_balance.lessons_balance:
                student_balance.lessons_balance = self.lesson_count
            else:
                student_balance.lessons_balance += self.lesson_count
        else:
            if not student_balance.bonus_lessons_balance:
                student_balance.bonus_lessons_balance = self.lesson_count
            else:
                student_balance.bonus_lessons_balance += self.lesson_count
        student_balance.save()
        return super(HistoryPaymentStudent, self).save(*args, **kwargs)


class TeacherRate(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель',
                                limit_choices_to={'is_teacher': True})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    rate = models.IntegerField(verbose_name='Ставка')

    class Meta:
        verbose_name = 'Ставка учителя'
        verbose_name_plural = 'Ставка учителя'

    def save(self, *args, **kwargs):
        user_rate = TeacherRate.objects.filter(teacher=self.teacher).select_related()
        if len(user_rate) == 0:
            super(TeacherRate, self).save(*args, **kwargs)
        else:
            for sub in user_rate.values('subject'):
                if sub['subject'] == self.subject.pk:
                    TeacherRate.objects.get(subject=self.subject).delete()
            super(TeacherRate, self).save(*args, **kwargs)


class HistoryPaymentTeacher(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель',
                                limit_choices_to={'is_teacher': True})
    payment_date = models.DateTimeField(verbose_name='Дата и время зачисления или снятия')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', **NULLABLE)
    amount = models.IntegerField(verbose_name='Сумма зачисления или снятия', **NULLABLE)
    currency = models.CharField(verbose_name='Валюта', choices=CURRENCY_CHOICES, default=TENGE, max_length=5)
    referral = models.BooleanField(verbose_name='Реферальная программа', default=False)

    class Meta:
        verbose_name = 'История операций учителя'
        verbose_name_plural = 'История операций учителя'

    def save(self, *args, **kwargs):
        teacher_balance = TeacherBalance.objects.filter(user=self.teacher).first()
        if not self.referral:
            if not teacher_balance.money_balance:
                teacher_balance.money_balance = self.amount
                ref_user = ReferralPromo.objects.filter(user=self.teacher).first()
                print(ref_user)
                lesson_count = ReferralSettings.objects.all().first().lesson_count
                amount = ReferralSettings.objects.all().first().amount
                if ref_user.from_user and not ref_user.is_used:
                    print(ref_user.from_user)
                    if ref_user.from_user.is_student:
                        HistoryPaymentStudent.objects.create(student=ref_user.from_user,
                                                             payment_date=datetime.datetime.now(),
                                                             lesson_count=lesson_count, referral=True)
                        ref_user.is_used = True
                        ref_user.save()
                    elif ref_user.from_user.is_teacher:
                        HistoryPaymentTeacher.objects.create(teacher=ref_user.from_user,
                                                             payment_date=datetime.datetime.now(),
                                                             amount=amount,
                                                             referral=True)
                        ref_user.is_used = True
                        ref_user.save()
                elif ref_user.from_user_link and not ref_user.is_used:
                    link = ref_user.from_user_link
                    user = ReferralPromo.objects.filter(user_link=link).first().user
                    if user.is_student:
                        HistoryPaymentStudent.objects.create(student=user, payment_date=datetime.datetime.now(),
                                                             lesson_count=lesson_count, referral=True)
                        ref_user.is_used = True
                        ref_user.save()
                    elif user.is_teacher:
                        HistoryPaymentTeacher.objects.create(teacher=user, payment_date=datetime.datetime.now(),
                                                             amount=amount,
                                                             referral=True)
                        ref_user.is_used = True
                        ref_user.save()
            else:
                if self.amount < 0:
                    if not teacher_balance.withdrawal_money:
                        teacher_balance.withdrawal_money = abs(self.amount)
                    else:
                        teacher_balance.withdrawal_money += abs(self.amount)
                teacher_balance.money_balance += self.amount
        else:
            if not teacher_balance.bonus_money_balance:
                teacher_balance.bonus_money_balance = self.amount
            else:
                teacher_balance.bonus_money_balance += self.amount
        teacher_balance.save()
        return super(HistoryPaymentTeacher, self).save(*args, **kwargs)
