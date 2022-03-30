from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import User
from finance.models import StudentBalance, HistoryPaymentStudent, TeacherBankData, TeacherBalance, HistoryPaymentTeacher
from finance.serializers import StudentBalanceSerializer, HistoryPaymentStudentSerializer, BillSerializer, \
    TeacherBalanceSerializer, HistoryPaymentTeacherSerializer


class BalanceListView(generics.ListAPIView):
    """Баланс пользователя"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = StudentBalance.objects.filter(user=user)
        else:
            queryset = TeacherBalance.objects.filter(user=user)
        return queryset

    def get_serializer_class(self):
        user = self.request.user
        if user.is_student:
            return StudentBalanceSerializer
        else:
            return TeacherBalanceSerializer


class StudentHistoryPayment(generics.ListAPIView):
    """История операций ученика"""
    permission_classes = [IsAuthenticated]
    serializer_class = HistoryPaymentStudentSerializer

    def get_queryset(self):
        user = self.request.user
        if self.request.query_params.get('subject') and self.request.query_params.get(
                'from') and self.request.query_params.get('status'):
            if self.request.query_params.get('status') == 'Списание':
                queryset = HistoryPaymentStudent.objects.filter(student=user,
                                                                subject__name=self.request.query_params.get('subject'),
                                                                payment_date__range=[
                                                                    self.request.query_params.get('from'),
                                                                    self.request.query_params.get(
                                                                        'to')], debit=True).order_by('-payment_date')
                return queryset
            else:
                queryset = HistoryPaymentStudent.objects.filter(student=user,
                                                                subject__name=self.request.query_params.get('subject'),
                                                                payment_date__range=[
                                                                    self.request.query_params.get('from'),
                                                                    self.request.query_params.get(
                                                                        'to')], debit=False).order_by('-payment_date')
                return queryset
        elif self.request.query_params.get('subject') and self.request.query_params.get('from'):
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
        elif self.request.query_params.get('status'):
            if self.request.query_params.get('status') == 'Списание':
                queryset = HistoryPaymentStudent.objects.filter(student=user,
                                                                debit=True).order_by('-payment_date')
                return queryset
            else:
                queryset = HistoryPaymentStudent.objects.filter(student=user,
                                                                debit=False).order_by('-payment_date')
                return queryset
        queryset = HistoryPaymentStudent.objects.filter(student=user).order_by('-payment_date')
        return queryset


class TeacherHistoryPayment(generics.ListAPIView):
    """История операций учителя"""
    permission_classes = [IsAuthenticated]
    serializer_class = HistoryPaymentTeacherSerializer

    def get_queryset(self):
        user = self.request.user
        if self.request.query_params.get('subject') and self.request.query_params.get(
                'from') and self.request.query_params.get('status'):
            if self.request.query_params.get('status') == 'Зачисление':
                queryset = HistoryPaymentTeacher.objects.filter(teacher=user,
                                                                lesson__subject__name=self.request.query_params.get(
                                                                    'subject'),
                                                                payment_date__range=[
                                                                    self.request.query_params.get('from'),
                                                                    self.request.query_params.get(
                                                                        'to')], is_enrollment=True).order_by(
                    '-payment_date')
                return queryset
            else:
                queryset = HistoryPaymentTeacher.objects.filter(teacher=user,
                                                                lesson__subject__name=self.request.query_params.get(
                                                                    'subject'),
                                                                payment_date__range=[
                                                                    self.request.query_params.get('from'),
                                                                    self.request.query_params.get(
                                                                        'to')], is_enrollment=False).order_by(
                    '-payment_date')
                return queryset

        if self.request.query_params.get('subject') and self.request.query_params.get('from'):
            queryset = HistoryPaymentTeacher.objects.filter(teacher=user,
                                                            lesson__subject__name=self.request.query_params.get(
                                                                'subject'),
                                                            payment_date__range=[self.request.query_params.get('from'),
                                                                                 self.request.query_params.get(
                                                                                     'to')]).order_by('-payment_date')
            return queryset
        elif self.request.query_params.get('subject'):
            queryset = HistoryPaymentTeacher.objects.filter(teacher=user,
                                                            lesson__subject__name=self.request.query_params.get(
                                                                'subject')).order_by('-payment_date')
            return queryset
        elif self.request.query_params.get('from'):
            queryset = HistoryPaymentTeacher.objects.filter(teacher=user,
                                                            payment_date__range=[
                                                                self.request.query_params.get('from'),
                                                                self.request.query_params.get(
                                                                    'to')]).order_by('-payment_date')
            return queryset
        elif self.request.query_params.get('status'):
            if self.request.query_params.get('status') == 'Зачисление':
                queryset = HistoryPaymentTeacher.objects.filter(teacher=user,
                                                                is_enrollment=True).order_by('-payment_date')
                return queryset
            else:
                queryset = HistoryPaymentTeacher.objects.filter(teacher=user,
                                                                is_enrollment=False).order_by('-payment_date')
                return queryset
        queryset = HistoryPaymentTeacher.objects.filter(teacher=user).order_by('-payment_date')
        return queryset


class BillUpdateView(generics.UpdateAPIView):
    """Обновление банковских данных учителя"""
    queryset = TeacherBankData.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BillSerializer
