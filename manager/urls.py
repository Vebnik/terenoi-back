from django.urls import path

from manager.apps import ManagerConfig
from manager.views import DashboardView, UsersListView, UsersCreateView, UsersTeacherListView, UsersManagerListView

app_name = ManagerConfig.name

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('users/', UsersListView.as_view(), name='users'),
    path('users/teacher/', UsersTeacherListView.as_view(), name='users_teachers'),
    path('users/manager/', UsersManagerListView.as_view(), name='users_managers'),
    path('users/create/', UsersCreateView.as_view(), name='users_create'),
]
