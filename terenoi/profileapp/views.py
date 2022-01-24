from django.shortcuts import render
from rest_framework import generics, permissions
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
        if self.request.user.is_student:
            return UpdateStudentSerializer
        elif self.request.user.is_teacher:
            return UpdateTeacherSerializer

    def update(self, request, *args, **kwargs):
        if request.data.get('subjects'):
            Subject.objects.create(user=self.request.user, subject=request.data.get('subjects'))
        return super(ProfileUpdateView, self).update(request, *args, **kwargs)


class ProfileRetrieveView(generics.RetrieveAPIView):
    permissions = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_student:
            return UpdateStudentSerializer
        else:
            return UpdateTeacherSerializer
