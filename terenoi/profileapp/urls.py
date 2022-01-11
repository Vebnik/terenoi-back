from django.urls import path
from profileapp.views import ProfileUpdateView

app_name = 'authapp'

urlpatterns = [
    path('update/', ProfileUpdateView.as_view(), name='update_profile')

]
