from django.urls import path

from finance.views import BalanceListView, StudentHistoryPayment

app_name = 'finance'

urlpatterns = [
    path('balance/', BalanceListView.as_view(), name='balance'),
    path('student-history-payments/', StudentHistoryPayment.as_view(), name='student_history_payments'),
]
