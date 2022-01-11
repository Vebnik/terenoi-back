from django.shortcuts import render
from rest_framework import generics, permissions
from authapp.models import User
from profileapp.models import Subject
from profileapp.permissions import IsStudent, IsTeacher
from profileapp.serializers import UpdateUserSerializer, UpdateStudentSerializer, UpdateTeacherSerializer


class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get_serializer_class(self):
        print()
        if self.request.user.role == 'ST':
            return UpdateStudentSerializer
        elif self.request.user.role == 'TH':
            return UpdateTeacherSerializer

    def update(self, request, *args, **kwargs):
        if request.data.get('subjects'):
            Subject.objects.create(user=self.request.user, subject=request.data.get('subjects'))
        return super(ProfileUpdateView, self).update(request, *args, **kwargs)
