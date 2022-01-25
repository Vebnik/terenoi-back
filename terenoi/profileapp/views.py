from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import User
from profileapp.models import Subject
from profileapp.permissions import IsStudent, IsTeacher
from profileapp.serializers import UpdateUserSerializer, UpdateStudentSerializer, UpdateTeacherSerializer


class ProfileUpdateView(generics.UpdateAPIView):
    """Редактирование пользователя"""
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get_serializer_class(self):
        user = self.get_object()
        if user.is_teacher or user.is_superuser:
            return UpdateTeacherSerializer
        else:
            return UpdateStudentSerializer

    def update(self, request, *args, **kwargs):
        if request.data.get('subjects'):
            Subject.objects.create(user=self.request.user, subject=request.data.get('subjects'))
        return super(ProfileUpdateView, self).update(request, *args, **kwargs)


class ProfileView(APIView):
    """Просмотр профиля пользователя"""
    permissions = (permissions.IsAuthenticated,)

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
