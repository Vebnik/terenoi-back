from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import User, VoxiAccount
from lessons.models import Lesson, LessonMaterials, LessonHomework, VoximplantRecordLesson
from lessons.serializers import UserLessonsSerializer, VoxiTeacherInfoSerializer, VoxiStudentInfoSerializer, \
    UserLessonsCreateSerializer, TeacherStatusUpdate, StudentStatusUpdate, LessonMaterialsSerializer, \
    LessonMaterialsDetail, LessonHomeworksDetail, LessonEvaluationSerializer, LessonStudentEvaluationAddSerializer, \
    LessonTeacherEvaluationAddSerializer
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

    def post(self, request, *args, **kwargs):
        if self.request.data.get('subject'):
            subject = Subject.objects.filter(name=self.request.data.get('subject')).first()
            if subject is None:
                return Response({"message": "Такого предмета не существует."}, status=status.HTTP_404_NOT_FOUND)

        return super(UserLessonCreateView, self).post(request, *args, **kwargs)


class LessonMaterialsAdd(generics.UpdateAPIView):
    """
    Добавление материалов урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer
    queryset = Lesson.objects.all()

    def put(self, request, *args, **kwargs):
        if self.request.FILES.getlist('material'):
            for material in self.request.FILES.getlist('material'):
                LessonMaterials.objects.create(lesson=self.get_object(), material=material)
        return super(LessonMaterialsAdd, self).put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if self.request.FILES.getlist('material'):
            for material in self.request.FILES.getlist('material'):
                LessonMaterials.objects.create(lesson=self.get_object(), material=material)
        return super(LessonMaterialsAdd, self).patch(request, *args, **kwargs)


class LessonHomeworksAdd(generics.UpdateAPIView):
    """
    Добавление домашних заданий урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer
    queryset = Lesson.objects.all()

    def put(self, request, *args, **kwargs):
        if self.request.FILES.getlist('homework'):
            for material in self.request.FILES.getlist('homework'):
                LessonHomework.objects.create(lesson=self.get_object(), homework=material)
        return super(LessonHomeworksAdd, self).put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if self.request.FILES.getlist('homework'):
            for material in self.request.FILES.getlist('homework'):
                LessonHomework.objects.create(lesson=self.get_object(), homework=material)
        return super(LessonHomeworksAdd, self).patch(request, *args, **kwargs)


class LessonMaterialsRetrieveView(generics.RetrieveAPIView):
    """
    Получение материалов урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LessonMaterialsDetail
    queryset = Lesson.objects.all()


class LessonHomeworksRetrieveView(generics.RetrieveAPIView):
    """
    Получение домашних заданий урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LessonHomeworksDetail
    queryset = Lesson.objects.all()


class LessonEvaluationRetrieveView(generics.RetrieveAPIView):
    """
    Просмотр оценки урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LessonEvaluationSerializer
    queryset = Lesson.objects.all()


class LessonEvaluationUpdateView(generics.UpdateAPIView):
    """
    Добавление оценки урока
    """
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_student:
            return LessonStudentEvaluationAddSerializer
        else:
            return LessonTeacherEvaluationAddSerializer


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


class CreateVoxiCallData(APIView):

    def post(self, request, *args, **kwargs):
        lesson_id = self.request.data.get('lesson_id')
        session_id = self.request.data.get('session_id')
        lesson = Lesson.objects.get(pk=int(lesson_id))
        VoximplantRecordLesson.objects.create(lesson=lesson, session_id=int(session_id))
        return Response({'message': 'Данные добавлены'}, status=status.HTTP_200_OK)
