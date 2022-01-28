from rest_framework import serializers

from lessons.services import current_date
from notifications.models import Notification


class UserNotificationsSerializer(serializers.ModelSerializer):
    current_created_at = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('pk', 'to_user', 'message', 'is_read', 'current_created_at')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_current_created_at(self, instance):
        user = self._user()
        date = current_date(user, instance.created_at)
        return date


class UserNotificationsUpdate(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('is_read',)
