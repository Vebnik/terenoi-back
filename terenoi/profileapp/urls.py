from django.urls import path
from profileapp.views import ProfileUpdateView, ProfileView, ReferralView, DeleteParentView, ChangePasswordView

app_name = 'profileapp'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('delete-parent/<int:pk>/', DeleteParentView.as_view(), name='delete_parent'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('ref/', ReferralView.as_view(), name='referral')

]
