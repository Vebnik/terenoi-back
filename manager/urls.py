from django.urls import path, re_path
from manager.apps import ManagerConfig

from manager.views import (
    DashboardView,
    UsersStudentListView,
    UsersCreateView,
    UsersTeacherListView,
    UsersManagerListView,
    UsersStudenSearchtListView,
    UsersStudenFiltertListView, 
    UsersUpdateView, 
    UserDetailView, 
    UsersManagerUpdateView,
    SubscriptionCreateView,
    SubscriptionUpdateView,
    ScheduleCreateView,
    ScheduleUpdateView,
    ScheduleGetTecherView,
    ######## DRF ########
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
    path('', DashboardView.as_view(), name='dashboard'),

    path('users/', UsersStudentListView.as_view(), name='users'),
    path('users/search/', UsersStudenSearchtListView.as_view(), name='users_search'),

    path('users/teacher/', UsersTeacherListView.as_view(), name='users_teachers'),
    path('users/manager/', UsersManagerListView.as_view(), name='users_managers'),
    path('users/filter/', UsersStudenFiltertListView.as_view(), name='user_filter'),

    path('users/create/', UsersCreateView.as_view(), name='users_create'),
    path('users/update/<int:pk>/', UsersUpdateView.as_view(), name='users_update'),
    path('users/update_manager/<int:pk>/', UsersManagerUpdateView.as_view(), name='users_update_manager'),

    path('users/detail/<int:pk>/', UserDetailView.as_view(), name='users_detail'),
    path('users/detail/subscription/<int:pk>/', UserDetailView.as_view(), name='users_detail_subscription'),
    path('users/detail/schedule/<int:pk>/', UserDetailView.as_view(), name='users_detail_schedule'),

    path('users/subscription/create/', SubscriptionCreateView.as_view(), name='sub_create'),
    path('users/subscription/update/<int:pk>/', SubscriptionUpdateView.as_view(), name='sub_update'),

    path('users/schedule/create/', ScheduleCreateView.as_view(), name='schedule_create'),
    path('users/schedule/update/<int:pk>/', ScheduleUpdateView.as_view(), name='schedule_update'),

    path('users/api/teacher/', ScheduleGetTecherView.as_view()),

    ########## DRF TEST ##########

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
