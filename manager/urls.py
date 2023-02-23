from django.urls import path, re_path
from manager.apps import ManagerConfig

from manager.views import (
    ManagerTemplateView,

    UserListApiView,
    UserCreateAPIView,
    UsersListApiView,
    UserUpdateAPIView,
    UserDetailApiView,

    SubscriptionListApiView,
    SubscriptionUpdateApiView,
)

app_name = ManagerConfig.name

urlpatterns = [
    ## react path ##
    path('', ManagerTemplateView.as_view(), name='index'),
    path('user/list/', ManagerTemplateView.as_view(), name='index'),
    path('user/add/', ManagerTemplateView.as_view(), name='index'),

    ## API ##
    re_path(r'users/students/', UserListApiView.as_view(), name='students_list'),
    re_path(r'users/list/', UsersListApiView.as_view(), name='users_list'),
    re_path(r'users/add/', UserCreateAPIView.as_view(), name='users_add'),
    path('users/update/<int:pk>', UserUpdateAPIView.as_view(), name='users_update'),
    path('users/detail/<int:pk>', UserDetailApiView.as_view(), name='users_detail'),

    path('subscriptions/list/', SubscriptionListApiView.as_view(), name='subscription_list'),
    path('subscription/update/<int:pk>/', SubscriptionUpdateApiView.as_view(), name='subscription_update'),
]
