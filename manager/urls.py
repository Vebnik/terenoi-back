from django.urls import path
from manager.apps import ManagerConfig

from manager.views import \
    DashboardView, \
    UsersStudentListView, \
    UsersCreateView, \
    UsersTeacherListView, \
    UsersManagerListView, \
    UsersStudenSearchtListView


app_name = ManagerConfig.name

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('users/', UsersStudentListView.as_view(), name='users'),
    path('users/teacher/', UsersTeacherListView.as_view(), name='users_teachers'),
    path('users/manager/', UsersManagerListView.as_view(), name='users_managers'),
    path('users/create/', UsersCreateView.as_view(), name='users_create'),
    path('users/search/', UsersStudenSearchtListView.as_view(), name='users_search'),
]
