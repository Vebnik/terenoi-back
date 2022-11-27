from django.db.models import Q
from rest_framework import serializers

from finance.models import StudentBalance, HistoryPaymentStudent, TeacherBankData, TeacherBalance, \
    HistoryPaymentTeacher, TeacherRate
from lessons.models import Lesson
from lessons.services import current_date
from profileapp.models import TeacherSubject
from settings.models import RateTeachers


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
        lessons_count = Lesson.objects.filter(students=user).exclude(
            Q(lesson_status=Lesson.RESCHEDULED) & Q(lesson_status=Lesson.CANCEL)).count()
        lessons_count_done = Lesson.objects.filter(students=user, lesson_status=Lesson.DONE).count()
        lesson = Lesson.objects.filter(students=user).order_by('-date')[:1].first()
        if not lesson:
            return 0
        lesson_date = Lesson.objects.filter(students=user).order_by('-date')[:1].first().date
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


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherBankData
        fields = ('pk', 'bank_name', 'bik', 'bill', 'full_teacher_name', 'card')


class TeacherBalanceSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    bill = serializers.SerializerMethodField()

    class Meta:
        model = TeacherBalance
        fields = ('money_balance', 'currency', 'date', 'rate', 'bill')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_date(self, instance):
        user_date = HistoryPaymentTeacher.objects.filter(teacher=self._user()).first()
        if not user_date:
            return None
        else:
            date = HistoryPaymentTeacher.objects.filter(teacher=self._user()).order_by(
                '-payment_date').first().payment_date
            return date.date()

    def get_rate(self, instance):
        data = []
        teacher_subject = TeacherSubject.objects.filter(user=self._user())
        teacher_rate = TeacherRate.objects.filter(teacher=self._user())
        if not teacher_subject:
            return None
        else:
            if not teacher_rate:
                for subj in teacher_subject:
                    default_rate = RateTeachers.objects.filter(subject=subj.subject).first().rate
                    data.append({
                        'subject': subj.subject.name,
                        'rate': default_rate
                    })
            else:
                for subj in teacher_subject:
                    try:
                        t_rate = TeacherRate.objects.filter(teacher=self._user(), subject=subj.subject).first().rate
                        data.append({
                            'subject': subj.subject.name,
                            'rate': t_rate
                        })
                    except Exception:
                        default_rate = RateTeachers.objects.filter(subject=subj.subject).first().rate
                        data.append({
                            'subject': subj.subject.name,
                            'rate': default_rate
                        })

        return data

    def get_bill(self, instance):
        bill = TeacherBankData.objects.filter(user=self._user()).first()
        serializer = BillSerializer(bill)
        return serializer.data


class HistoryPaymentTeacherSerializer(serializers.ModelSerializer):
    current_date = serializers.SerializerMethodField()
    current_time = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = HistoryPaymentTeacher
        fields = ('current_date', 'current_time', 'amount', 'subject_name', 'action', 'status')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_action(self, instance):
        if instance.is_enrollment:
            return 'Зачисление'
        elif instance.referral:
            return 'Зачисление реферальной программы'
        else:
            return 'Вывод средств'

    def get_status(self, instance):
        return 'Успешно'

    def get_current_date(self, instance):
        user = self._user()
        date = current_date(user, instance.payment_date)
        return date.date()

    def get_current_time(self, instance):
        user = self._user()
        date = current_date(user, instance.payment_date)
        return date.time()

    def get_subject_name(self, instance):
        if instance.lesson.subject:
            return instance.lesson.subject.name
        else:
            return None
