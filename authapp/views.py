from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, permissions, views, authentication
import jwt
from rest_framework.response import Response
from authapp.models import User
from authapp.serializers import UserRegisterSerializer, VerifyEmailSerializer, UserWhoiAmSerializer
from authapp.services import send_verify_email
from notifications.models import ManagerNotification
from profileapp.models import ReferralPromo
from profileapp.services import generateRefPromo


class UserRegister(generics.CreateAPIView):
    """"Регистрация пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        managers = User.objects.filter(is_staff=True)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Неправильный email или пароль'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        send_verify_email(user)
        for manager in managers:
            ManagerNotification.objects.create(manager=manager, type=ManagerNotification.NEW_USER)
        return Response({
            "message": "Пользователь зарегистрирован, осталось пройти верификацию почты."},
            status=status.HTTP_201_CREATED
        )


class VerifyEmail(generics.GenericAPIView):
    """Верификация пользователя по эмейлу"""
    serializer_class = VerifyEmailSerializer
    permission_classes = [permissions.AllowAny]
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='token', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"email": "Почта активированна"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Ошибка активации"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"error": "Неверный токен"}, status=status.HTTP_400_BAD_REQUEST)


class WhoiAm(views.APIView):
    """Получения информации о пользователе текущей сессии"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            user = UserWhoiAmSerializer(request.user)
            return Response(user.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
