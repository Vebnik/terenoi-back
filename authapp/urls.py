from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from authapp.serializers import UserLoginSerializer
from authapp.views import UserRegister, VerifyEmail, WhoiAm

app_name = 'authapp'

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(serializer_class=UserLoginSerializer), name='login'),
    path('verify-email/', VerifyEmail.as_view(), name='verify_email'),

    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('whoiam/', WhoiAm.as_view(), name='whoiam')

]
