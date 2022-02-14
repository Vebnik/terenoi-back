from django.urls import path
from profileapp.views import ProfileUpdateView, ProfileView, ReferralView

app_name = 'authapp'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),

    path('ref/',ReferralView.as_view(),name='referral')

]
