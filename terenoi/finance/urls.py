from django.urls import path

from finance.views import BalanceListView, StudentHistoryPayment, BillUpdateView, TeacherHistoryPayment

app_name = 'finance'

urlpatterns = [
    path('balance/', BalanceListView.as_view(), name='balance'),
    path('student-history-payments/', StudentHistoryPayment.as_view(), name='student_history_payments'),
    path('teacher-history-payments/', TeacherHistoryPayment.as_view(), name='teacher_history_payments'),

    path('bill/update/', BillUpdateView.as_view(), name='bill_update'),
]
