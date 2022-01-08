from django.conf import settings
from rest_framework import generics, status, permissions
import jwt
from rest_framework.response import Response
from authapp.models import User
from authapp.serializers import UserRegisterSerializer, VerifyEmailSerializer
from authapp.services import send_verify_email


class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Неправильный email или пароль'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        send_verify_email(user)
        return Response({
            "message": "Пользователь зарегистрирован, осталось пройти верификацию почты."},
            status=status.HTTP_201_CREATED
        )


class VerifyEmail(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def get(self, request):
        token = request.data.get('token')
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



