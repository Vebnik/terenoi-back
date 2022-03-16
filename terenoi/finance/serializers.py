from django.db.models import Sum, Q
from rest_framework import serializers

from finance.models import StudentBalance, HistoryPaymentStudent
from lessons.models import Lesson
from lessons.services import current_date
from profileapp.models import Subject


class StudentBalanceSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = StudentBalance
        fields = ('user', 'money_balance', 'lessons_count', 'currency', 'lessons_balance', 'bonus_lessons_balance')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_lessons_count(self, instance):
        user = self._user()
        lessons_count = Lesson.objects.filter(student=user).exclude(
            Q(lesson_status=Lesson.RESCHEDULED) & Q(lesson_status=Lesson.CANCEL)).count()
        lessons_count_done = Lesson.objects.filter(student=user, lesson_status=Lesson.DONE).count()
        lesson_date = Lesson.objects.filter(student=user).order_by('-date')[:1].first().date
        date = current_date(user=user, date=lesson_date)
        return [lessons_count, lessons_count_done, date.date()]


class HistoryPaymentStudentSerializer(serializers.ModelSerializer):
    current_date = serializers.SerializerMethodField()
    current_time = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()

    class Meta:
        model = HistoryPaymentStudent
        fields = ('current_date', 'current_time', 'lesson_count', 'subject_name', 'status')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_status(self, instance):
        if instance.debit:
            return 'Списание'
        elif instance.referral:
            return 'Зачисление реферальной программы'
        else:
            return 'Зачисление'

    def get_current_date(self, instance):
        user = self._user()
        date = current_date(user, instance.payment_date)
        return date.date()

    def get_current_time(self, instance):
        user = self._user()
        date = current_date(user, instance.payment_date)
        return date.time()

    def get_subject_name(self, instance):
        if instance.subject:
            return instance.subject.name
        else:
            return None
