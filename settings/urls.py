from django.urls import path

from settings.views import CitiesListView

app_name = 'settings'

urlpatterns = [
    path('cities/', CitiesListView.as_view(), name='cities'),
]
