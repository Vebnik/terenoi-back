from django.urls import path
from notifications.views import UserNotificationListView, UserAllNotificationsUpdateView, UserNotificationUpdateView, \
    UserAllNotificationListView

app_name = 'notifications'
urlpatterns = [
    path('', UserNotificationListView.as_view(), name='user_notifications'),
    path('all/', UserAllNotificationListView.as_view(), name='user_all_notifications'),
    path('update/', UserAllNotificationsUpdateView.as_view(), name='user_notifications_update_all'),
    path('update/<int:pk>/', UserNotificationUpdateView.as_view(), name='user_notifications_update'),
]
