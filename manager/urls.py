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
    StudentStatusUpdateApiView,

    SubscriptionListApiView,
    SubscriptionUpdateApiView,
    SubscriptionPaginateListApiView,
    SubscriptionCreateApiView,
)

app_name = ManagerConfig.name

urlpatterns = [
    # for dev test not endpoint
    path('', ManagerTemplateView.as_view(), name='index'),
    path('user/list/', ManagerTemplateView.as_view(), name='index'),
    path('user/add/', ManagerTemplateView.as_view(), name='index'),

    # student
    re_path(r'students/list/paginate/', StudentPaginateListApiView.as_view(), name='student_paginate_list'),
    re_path(r'student/add/', StudentCreateAPIView.as_view(), name='student_add'),
    path('students/update/<int:pk>', StudentUpdateAPIView.as_view(), name='students_update'),
    path('student/detail/<int:pk>', StudentDetailApiView.as_view(), name='users_detail'),
    path('students/update/status/<int:pk>/', StudentStatusUpdateApiView.as_view(), name='students_update_status'),
    
    # general
    re_path(r'users/list/', StudentsListApiView.as_view(), name='users_list'),

    # subs
    path('subscriptions/list/', SubscriptionListApiView.as_view(), name='subscription_list'),
    re_path(r'subscriptions/list/paginate/', SubscriptionPaginateListApiView.as_view(), name='subscription_paginate_list'),
    path('subscriptions/add/', SubscriptionCreateApiView.as_view(), name='subscription_add'),
    path('subscription/update/<int:pk>/', SubscriptionUpdateApiView.as_view(), name='subscription_update'),
]
