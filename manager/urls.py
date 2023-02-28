from django.urls import path, re_path
from manager.apps import ManagerConfig

from manager.views import (
    StudentPaginateListApiView,
    StudentDetailApiView,
    StudentUpdateAPIView,
    StudentCreateAPIView,
    StudentStatusUpdateApiView,

    SubscriptionListApiView,
    SubscriptionUpdateApiView,
    SubscriptionPaginateListApiView,
    SubscriptionCreateApiView,

    ManagerListApiView,
)

app_name = ManagerConfig.name

urlpatterns = [

    # student
    re_path(r'student/list/paginate/', StudentPaginateListApiView.as_view(), name='student_paginate_list'),
    re_path(r'student/add/', StudentCreateAPIView.as_view(), name='student_add'),
    path('student/update/<int:pk>/', StudentUpdateAPIView.as_view(), name='students_update'),
    path('student/detail/<int:pk>/', StudentDetailApiView.as_view(), name='users_detail'),
    path('student/update/status/<int:pk>/', StudentStatusUpdateApiView.as_view(), name='students_update_status'),
    
    # subscription
    path('subscriptions/list/', SubscriptionListApiView.as_view(), name='subscription_list'),
    re_path(r'subscriptions/list/paginate/', SubscriptionPaginateListApiView.as_view(), name='subscription_paginate_list'),
    path('subscriptions/add/', SubscriptionCreateApiView.as_view(), name='subscription_add'),
    path('subscription/update/<int:pk>/', SubscriptionUpdateApiView.as_view(), name='subscription_update'),

    # manager
    path('manager/list/', ManagerListApiView.as_view(), name='manager_list')
]
