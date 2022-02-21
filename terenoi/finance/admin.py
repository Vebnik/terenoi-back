from django.contrib import admin

# Register your models here.
from finance.models import StudentBalance, TeacherBalance, HistoryPaymentStudent, HistoryPaymentTeacher


@admin.register(StudentBalance)
class StudentBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'money_balance', 'currency', 'lessons_balance', 'bonus_lessons_balance')


@admin.register(TeacherBalance)
class TeacherBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'money_balance', 'currency', 'bonus_money_balance', 'withdrawal_money')


@admin.register(HistoryPaymentStudent)
class HistoryPaymentStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'manager', 'payment_date', 'amount', 'currency', 'subject', 'lesson_count', 'referral')


@admin.register(HistoryPaymentTeacher)
class HistoryPaymentTeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'payment_date', 'lesson', 'amount', 'currency', 'referral')
