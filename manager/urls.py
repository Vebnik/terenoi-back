from django.urls import path

from manager.apps import ManagerConfig
from manager.views import DashboardView

app_name = ManagerConfig.name

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard')
]
