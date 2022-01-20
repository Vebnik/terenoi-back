from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from authapp.models import User
from lessons.models import Lesson
from lessons.serializers import UserLessonsSerializer


class AllUserLessonsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == User.STUDENT:
            queryset = Lesson.objects.filter(student=self.request.user)
        else:
            queryset = Lesson.objects.filter(teacher=self.request.user)
        return queryset


class UserLessonRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer
    queryset = Lesson.objects.all()
