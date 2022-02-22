from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authapp.models import User
from profileapp.models import TeacherSubject, Subject, ReferralPromo
from profileapp.permissions import IsStudent, IsTeacher
from profileapp.serializers import UpdateUserSerializer, UpdateStudentSerializer, UpdateTeacherSerializer, \
    ReferralSerializer


class ProfileUpdateView(generics.UpdateAPIView):
    """Редактирование пользователя"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get_serializer_class(self):
        user = self.get_object()
        if user.is_teacher or user.is_superuser:
            return UpdateTeacherSerializer
        else:
            return UpdateStudentSerializer

    def update(self, request, *args, **kwargs):
        try:
            if request.data.get('subject'):
                for sub in request.data.get('subject'):
                    subject = Subject.objects.filter(name=sub).first()
                    if subject:
                        TeacherSubject.objects.create(user=self.request.user, subject=subject)
                        return super(ProfileUpdateView, self).update(request, *args, **kwargs)
                else:
                    return Response({"message": "Такого предмета не существует."}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return super(ProfileUpdateView, self).update(request, *args, **kwargs)


class ProfileView(APIView):
    """Просмотр профиля пользователя"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request):
        user = self.get_object()
        if user.is_teacher or user.is_superuser:
            serializer = UpdateTeacherSerializer(user)
            return Response(serializer.data)
        else:
            serializer = UpdateStudentSerializer(user)
            return Response(serializer.data)


class ReferralView(APIView):
    """Получение реферального кода"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request):
        user = self.get_object()
        promo = ReferralPromo.objects.filter(user=user).first()
        serializer = ReferralSerializer(promo)
        return Response(serializer.data)

