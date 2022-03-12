from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import User
from finance.models import StudentBalance, HistoryPaymentStudent
from finance.serializers import StudentBalanceSerializer, HistoryPaymentStudentSerializer


class BalanceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentBalanceSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = StudentBalance.objects.filter(user=user)
        return queryset


class StudentHistoryPayment(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HistoryPaymentStudentSerializer

    def get_queryset(self):
        user = self.request.user
        if self.request.query_params.get('subject') and self.request.query_params.get('from'):
            queryset = HistoryPaymentStudent.objects.filter(student=user,
                                                            subject__name=self.request.query_params.get('subject'),
                                                            payment_date__range=[self.request.query_params.get('from'),
                                                                                 self.request.query_params.get(
                                                                                     'to')]).order_by('-payment_date')
            return queryset
        elif self.request.query_params.get('subject'):
            queryset = HistoryPaymentStudent.objects.filter(student=user,
                                                            subject__name=self.request.query_params.get(
                                                                'subject')).order_by('-payment_date')
            return queryset
        elif self.request.query_params.get('from'):
            queryset = HistoryPaymentStudent.objects.filter(student=user,
                                                            payment_date__range=[self.request.query_params.get('from'),
                                                                                 self.request.query_params.get(
                                                                                     'to')]).order_by('-payment_date')
            return queryset
        queryset = HistoryPaymentStudent.objects.filter(student=user).order_by('-payment_date')
        return queryset
