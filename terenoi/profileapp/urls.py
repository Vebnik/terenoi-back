from django.urls import path
from profileapp.views import ProfileUpdateView, ProfileView, ReferralView, DeleteParentView, ChangePasswordView, \
    ProfileUpdateAvatarView, HelpView

app_name = 'profileapp'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('update/avatar/', ProfileUpdateAvatarView.as_view(), name='update_avatar'),
    path('delete-parent/<int:pk>/', DeleteParentView.as_view(), name='delete_parent'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('ref/', ReferralView.as_view(), name='referral'),

    path('help/', HelpView.as_view(), name='help'),

]
