from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from authapp.models import User
from courses.models import Courses, LessonCourse, CourseWishList
from courses.serializers import CourseSerializer, CourseRetrieveSerializer, LessonsCourseAllSerializer, \
    LessonsCourseRetrieveSerializer, WishListSerializer


class AllCoursesListView(generics.ListAPIView):
    """Список всех курсов"""
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()


class CoursesRetrieveView(generics.RetrieveAPIView):
    """Просмотр одного курса"""
    permission_classes = [IsAuthenticated]
    serializer_class = CourseRetrieveSerializer
    queryset = Courses.objects.all()


class LessonsCourseAllView(generics.ListAPIView):
    """Отображение всех уроков курса"""
    permission_classes = [IsAuthenticated]
    serializer_class = LessonsCourseAllSerializer

    def get_queryset(self):
        course = int(self.kwargs.get('pk'))
        return LessonCourse.objects.filter(course__pk=course)


class LessonCourseRetrieveView(generics.RetrieveAPIView):
    """Просмотр одного урока курса"""
    permission_classes = [IsAuthenticated]
    serializer_class = LessonsCourseRetrieveSerializer
    queryset = LessonCourse.objects.all()


class AddCourseWishListView(APIView):
    """Добавление курса в вишлист"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def post(self, request):
        user = self.get_object()
        course = Courses.objects.filter(pk=self.request.data.get('pk')).first()
        if course:
            CourseWishList.objects.create(user=user, course=course)
            data = {'message': True}
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            data = {'message': False}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


class DeleteCourseWishListView(APIView):
    """Удаление курса из вишлиста"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def delete(self, request):
        user = self.get_object()
        course = Courses.objects.filter(pk=self.request.data.get('pk')).first()
        wish = CourseWishList.objects.filter(user=user, course=course)
        if course and wish:
            wish.delete()
            data = {'message': True}
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            data = {'message': False}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


class WishListView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishListSerializer
    queryset = CourseWishList.objects.all()

    def get_serializer(self, *args, **kwargs):
        return WishListSerializer(self.queryset, context={'pk': self.kwargs.get('pk')})



