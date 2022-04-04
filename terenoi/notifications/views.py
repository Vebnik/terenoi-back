from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.models import Notification, HomeworkNotification, LessonRateNotification, PaymentNotification
from notifications.serializers import UserNotificationsSerializer, UserNotificationsUpdate, UserNotificationsAllUpdate


class PublicationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserNotificationListView(generics.ListAPIView):
    """Просмотр всех непрочитаных уведомлений пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationsSerializer

    def get_queryset(self):
        user = self.request.user
        queryset_homework = HomeworkNotification.objects.filter((Q(to_user=user) & Q(is_read=False))).select_related()
        queryset_rate = LessonRateNotification.objects.filter((Q(to_user=user) & Q(is_read=False))).select_related()
        queryset_payment = PaymentNotification.objects.filter((Q(to_user=user) & Q(is_read=False))).select_related()
        queryset = Notification.objects.filter((Q(to_user=user) & Q(is_read=False))).select_related()
        queryset_all = queryset.union(queryset_homework, queryset_rate, queryset_payment).order_by('-created_at')
        return queryset_all


class UserAllNotificationListView(generics.ListAPIView):
    """Получение всех уведомлений пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationsSerializer
    pagination_class = PublicationPagination

    def get_queryset(self):
        user = self.request.user
        queryset_homework = HomeworkNotification.objects.filter((Q(to_user=user) & Q(is_read=False))).select_related()
        queryset_rate = LessonRateNotification.objects.filter((Q(to_user=user) & Q(is_read=False))).select_related()
        queryset_payment = PaymentNotification.objects.filter((Q(to_user=user) & Q(is_read=False))).select_related()
        queryset = Notification.objects.filter(Q(to_user=user) & Q(is_read=False)).select_related()
        queryset_all = queryset.union(queryset_homework, queryset_rate, queryset_payment).order_by('-created_at')
        return queryset_all


class UserAllNotificationsUpdateView(generics.UpdateAPIView):
    """Обновление всех непрочитаных уведомлений пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationsAllUpdate
    queryset = Notification.objects.all()

    def patch(self, request, *args, **kwargs):
        queryset_homework = HomeworkNotification.objects.filter(
            (Q(to_user=request.user) & Q(is_read=False))).select_related()
        queryset_rate = LessonRateNotification.objects.filter(
            (Q(to_user=request.user) & Q(is_read=False))).select_related()
        queryset = Notification.objects.filter(to_user=request.user).select_related()
        queryset_all = queryset.union(queryset_homework, queryset_rate)
        queryset_all.update(is_read=True)
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        queryset_homework = HomeworkNotification.objects.filter(
            (Q(to_user=request.user) & Q(is_read=False))).select_related()
        queryset_rate = LessonRateNotification.objects.filter(
            (Q(to_user=request.user) & Q(is_read=False))).select_related()
        queryset = Notification.objects.filter(to_user=request.user).select_related()
        queryset_all = queryset.union(queryset_homework, queryset_rate)
        queryset_all.update(is_read=True)
        return Response(status=status.HTTP_200_OK)


class UserNotificationUpdateView(generics.UpdateAPIView):
    """Обновление одного непрочитаного уведомления пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationsUpdate

    def get_queryset(self):
        user = self.request.user
        queryset_homework = HomeworkNotification.objects.filter((Q(to_user=user) & Q(is_read=False))).select_related()
        queryset_rate = LessonRateNotification.objects.filter((Q(to_user=user) & Q(is_read=False))).select_related()
        queryset = Notification.objects.filter(to_user=user).select_related()
        queryset_all = queryset.union(queryset_homework, queryset_rate)
        return queryset_all
