from django.contrib import admin

# Register your models here.
from finance.models import ( 
    StudentBalance, TeacherBalance, 
    HistoryPaymentStudent, HistoryPaymentTeacher, 
    TeacherRate, TeacherBankData, 
    PaymentMethod, StudentSubscription,
)


@admin.register(StudentBalance)
class StudentBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'money_balance', 'currency', 'lessons_balance', 'bonus_lessons_balance')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


@admin.register(TeacherBalance)
class TeacherBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'money_balance', 'currency', 'bonus_money_balance', 'withdrawal_money')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


@admin.register(TeacherRate)
class TeacherRateAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'rate')
    search_fields = ['teacher__username', 'teacher__first_name', 'teacher__last_name']


@admin.register(HistoryPaymentStudent)
class HistoryPaymentStudentAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'manager', 'payment_date', 'amount', 'currency', 'subject', 'lesson_count', 'invoice', 'debit',
        'referral')
    list_filter = ('debit', 'subject', 'referral')
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'manager__username',
                     'manager__first_name', 'manager__last_name']
    date_hierarchy = 'payment_date'


@admin.register(HistoryPaymentTeacher)
class HistoryPaymentTeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'payment_date', 'lesson', 'amount', 'currency', 'invoice', 'is_enrollment', 'referral')
    list_filter = ('is_enrollment', 'referral')
    search_fields = ['teacher__username', 'teacher__first_name', 'teacher__last_name']
    date_hierarchy = 'payment_date'


@admin.register(TeacherBankData)
class TeacherBankDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank_name', 'bik', 'full_teacher_name')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('title', )

@admin.register(StudentSubscription)
class StudentSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('payment_methods','student','title','plan_type','billing','lesson_count','lesson_duration','lesson_cost','subscription_cost', )