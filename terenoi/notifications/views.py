from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.models import Notification
from notifications.serializers import UserNotificationsSerializer, UserNotificationsUpdate


class UserNotificationListView(generics.ListAPIView):
    """Просмотр всех непрочитаных уведомлений пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationsSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter((Q(to_user=user) & Q(is_read=False))).order_by(
            '-created_at').select_related()
        return queryset


class UserAllNotificationsUpdateView(generics.UpdateAPIView):
    """Обновление всех непрочитаных уведомлений пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationsUpdate
    queryset = Notification.objects.all()

    def patch(self, request, *args, **kwargs):
        notif_list = Notification.objects.filter((Q(to_user=request.user) & Q(is_read=False))).select_related()
        notif_list.update(is_read=True)
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        notif_list = Notification.objects.filter((Q(to_user=request.user) & Q(is_read=False))).select_related()
        notif_list.update(is_read=True)
        return Response(status=status.HTTP_200_OK)


class UserNotificationUpdateView(generics.UpdateAPIView):
    """Обновление одного непрочитаного уведомления пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationsUpdate
    queryset = Notification.objects.all()


