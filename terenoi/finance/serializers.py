from rest_framework import serializers

from finance.models import StudentBalance, HistoryPaymentStudent
from lessons.services import current_date
from profileapp.models import Subject


class StudentBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentBalance
        fields = ('user', 'money_balance', 'currency', 'lessons_balance', 'bonus_lessons_balance')


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

    def get_status(self, instace):
        if instace.debit:
            return 'Списание'
        elif instace.referral:
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
