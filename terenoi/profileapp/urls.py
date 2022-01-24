from django.urls import path
from profileapp.views import ProfileUpdateView, ProfileRetrieveView

app_name = 'authapp'

urlpatterns = [
    path('<int:pk>/',ProfileRetrieveView.as_view(),name='profile'),
    path('update/', ProfileUpdateView.as_view(), name='update_profile')

]
