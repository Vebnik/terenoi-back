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

    ScheduleCreateApiView,
    ScheduleDestroyApiView,
    ScheduleExistGroupCreateApiView,
    ScheduleGroupCreateApiView,

    ManagerListApiView,

    TeacherListApiView,

    SubjectListApiView,

    GroupListApiView,
    GroupDeleteUserDelteApiView,
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
    path('manager/list/', ManagerListApiView.as_view(), name='manager_list'),

    #schedule
    path('schedule/add/ind/', ScheduleCreateApiView.as_view(), name='schedule_add_individual'),
    path('schedule/add/group/', ScheduleGroupCreateApiView.as_view(), name='schedule_add_group'),
    path('schedule/add/groupex/', ScheduleExistGroupCreateApiView.as_view(), name='schedule_add_exist_group'),
    path('schedule/delete/<int:pk>/', ScheduleDestroyApiView.as_view(), name='schedule_delete'),

    #teacher
    path('teacher/list/', TeacherListApiView.as_view(), name='teacher_list'),
    re_path(r'teacher/list/', TeacherListApiView.as_view(), name='teacher_list_filter'),

    # group
    path('group/delete/user/', GroupDeleteUserDelteApiView.as_view(), name='group_delete_user'),
    path('group/list/', GroupListApiView.as_view(), name='group'),
    re_path(r'group/list/', GroupListApiView.as_view(), name='group_list_filter'),

    # utils
    path('subject/list/', SubjectListApiView.as_view(), name='subject_list')

]
