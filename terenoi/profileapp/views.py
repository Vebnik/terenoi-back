from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authapp.models import User
from profileapp.models import TeacherSubject, Subject
from profileapp.permissions import IsStudent, IsTeacher
from profileapp.serializers import UpdateUserSerializer, UpdateStudentSerializer, UpdateTeacherSerializer


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
            if request.data.get('subject').get('subject_name'):
                subjects = Subject.objects.filter(name=request.data.get('subject').get('subject_name')).select_related()
                if subjects:
                    for sub in subjects:
                        TeacherSubject.objects.create(user=self.request.user, subject=sub)
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
