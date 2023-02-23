from django.urls import path, re_path
from manager.apps import ManagerConfig

from manager.views import (
    ManagerTemplateView,

    StudentPaginateListApiView,
    StudentListApiView,
    StudentDetailApiView,
    StudentUpdateAPIView,
    StudentCreateAPIView,
    StudentsListApiView,

    SubscriptionListApiView,
    SubscriptionUpdateApiView,
    SubscriptionPaginateListApiView,
    SubscriptionCreateApiView,
)

app_name = ManagerConfig.name

urlpatterns = [
    ## for dev test ##
    path('', ManagerTemplateView.as_view(), name='index'),
    path('user/list/', ManagerTemplateView.as_view(), name='index'),
    path('user/add/', ManagerTemplateView.as_view(), name='index'),

    ## API ##
    re_path(r'students/list/paginate/', StudentPaginateListApiView.as_view(), name='stident_paginate_list'),
    re_path(r'users/students/', StudentListApiView.as_view(), name='students_list'),
    re_path(r'users/list/', StudentsListApiView.as_view(), name='users_list'),
    re_path(r'users/add/', StudentCreateAPIView.as_view(), name='users_add'),
    path('users/update/<int:pk>', StudentUpdateAPIView.as_view(), name='users_update'),
    path('users/detail/<int:pk>', StudentDetailApiView.as_view(), name='users_detail'),

    path('subscriptions/list/', SubscriptionListApiView.as_view(), name='subscription_list'),
    re_path(r'subscriptions/list/paginate/', SubscriptionPaginateListApiView.as_view(), name='subscription_paginate_list'),
    path('subscriptions/add/', SubscriptionCreateApiView.as_view(), name='subscription_add'),
    path('subscription/update/<int:pk>/', SubscriptionUpdateApiView.as_view(), name='subscription_update'),
]
