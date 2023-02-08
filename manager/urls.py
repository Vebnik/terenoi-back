from django.urls import path
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
    UsersManagerUpdateView
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
]
