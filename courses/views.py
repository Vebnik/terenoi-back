from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from courses.models import Courses, LessonCourse
from courses.serializers import CourseSerializer, CourseRetrieveSerializer, LessonsCourseAllSerializer, \
    LessonsCourseRetrieveSerializer


class AllCoursesListView(generics.ListAPIView):
    """Список всех уроков пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()


class CoursesRetrieveView(generics.RetrieveAPIView):
    """Просмотр одного урока пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = CourseRetrieveSerializer
    queryset = Courses.objects.all()


class LessonsCourseAllView(generics.ListAPIView):
    """Просмотр одного урока пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = LessonsCourseAllSerializer

    def get_queryset(self):
        course = int(self.kwargs.get('pk'))
        return LessonCourse.objects.filter(course__pk=course)


class LessonCourseRetrieveView(generics.RetrieveAPIView):
    """Просмотр одного урока пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = LessonsCourseRetrieveSerializer
    queryset = LessonCourse.objects.all()