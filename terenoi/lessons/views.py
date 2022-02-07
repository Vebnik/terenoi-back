from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response

from authapp.models import User, VoxiAccount
from lessons.models import Lesson
from lessons.serializers import UserLessonsSerializer, VoxiTeacherInfoSerializer, VoxiStudentInfoSerializer, \
    UserLessonsCreateSerializer, TeacherStatusUpdate, StudentStatusUpdate
from profileapp.models import Subject


class AllUserLessonsListView(generics.ListAPIView):
    """Список всех уроков пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = Lesson.objects.filter(student=self.request.user).order_by('date').select_related()
        else:
            queryset = Lesson.objects.filter(teacher=self.request.user).order_by('date').select_related()
        return queryset


class AllUserClassesListView(generics.ListAPIView):
    """Список всех прошедших уроков пользователя и одного будущего"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset_1 = Lesson.objects.filter(
                (Q(student=self.request.user) & Q(lesson_status=Lesson.DONE))).select_related()
            queryset_2 = Lesson.objects.filter(
                Q(student=self.request.user) & Q(lesson_status=Lesson.SCHEDULED)).order_by('date')[:1].select_related()
            queryset_3 = Lesson.objects.filter(
                (Q(student=self.request.user) & Q(lesson_status=Lesson.PROGRESS))).select_related()
            queryset = queryset_1.union(queryset_2, queryset_3).order_by('-date')

        else:
            queryset_1 = Lesson.objects.filter(
                (Q(teacher=self.request.user) & Q(lesson_status=Lesson.DONE))).select_related()
            queryset_2 = Lesson.objects.filter(
                Q(teacher=self.request.user) & Q(lesson_status=Lesson.SCHEDULED)).order_by('date')[:1].select_related()
            queryset_3 = Lesson.objects.filter(
                (Q(teacher=self.request.user) & Q(lesson_status=Lesson.PROGRESS))).select_related()
            queryset = queryset_1.union(queryset_2, queryset_3).order_by('-date')
        return queryset


class UserLessonRetrieveView(generics.RetrieveAPIView):
    """Просмотр одного урока пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer
    queryset = Lesson.objects.all()


class UserLessonCreateView(generics.CreateAPIView):
    """Создание урока"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsCreateSerializer
    queryset = Lesson.objects.all()

    def create(self, request, *args, **kwargs):
        file_fields = list(request.FILES.keys())
        serializer = self.get_serializer(data=request.data, file_fields=file_fields)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('subject'):
            subject = Subject.objects.filter(name=self.request.data.get('subject')).first()
            if subject is None:
                return Response({"message": "Такого предмета не существует."}, status=status.HTTP_404_NOT_FOUND)

        return super(UserLessonCreateView, self).post(request, *args, **kwargs)



class VoxiTeacherInfoRetrieveView(generics.RetrieveAPIView):
    """Информация об аккаунте учителя в voxiplant и статусе его готовности"""
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = VoxiTeacherInfoSerializer


class VoxiStudentInfoRetrieveView(generics.RetrieveAPIView):
    """Информация об аккаунте студента в voxiplant и статусе его готовности"""
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = VoxiStudentInfoSerializer


class LessonUserStatusUpdateView(generics.UpdateAPIView):
    """Обновление статуса пользователя в уроке"""
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_teacher:
            return TeacherStatusUpdate
        elif self.request.user.is_student:
            return StudentStatusUpdate


class LessonUpdateView(generics.UpdateAPIView):
    """Обновление данных урока"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer
    queryset = Lesson.objects.all()
