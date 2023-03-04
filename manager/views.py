from rest_framework import generics, permissions, authentication, status, response, views
from django.db.models import Q
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from json import loads

from authapp.models import User, Group
from manager.service import StandardResultsSetPagination, QueryParams, Filter, TeacherQueryParams
from finance.models import StudentSubscription
from profileapp.models import Subject
from lessons.models import Schedule

from manager.serializers import (
    UserSerializers, UserCreateUpdateSerializers, 
    UserDetailSerializers, SubscriptionListSerializers,
    StudentStatusSerializers, ManagerListSerializers,
    TeacherListSerializers, SubjectListSerializers,
    ScheduleCreateSerializers, GroupSerializer,
    ScheduleGroupCreateSerializers,
)


# student
class StudentPaginateListApiView(generics.ListAPIView):
    """
    API Endpoint for get users of authapp.User
    """
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializers
    queryset = User.objects.filter(is_student=True)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        params = QueryParams(self.request.GET)
        queryset = super().get_queryset()

        return Filter.students_filter(queryset, params)

    def get(self, request, *args, **kwargs):
        params = QueryParams(request.GET)
        self.pagination_class.page_size = params.perPage

        return super().get(request, *args, **kwargs)


class StudentListApiView(generics.ListAPIView):
    """
    API Endpoint for get users of authapp.User
    """
    # authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserSerializers
    queryset = User.objects.filter(is_student=True)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        params = QueryParams(self.request.GET)
        queryset = super().get_queryset()

        return Filter.students_filter(queryset, params)

    def get(self, request, *args, **kwargs):
        params = QueryParams(request.GET)
        self.pagination_class.page_size = params.perPage

        return super().get(request, *args, **kwargs)


class StudentCreateAPIView(generics.CreateAPIView):
    """
    API Endpoint for create users of authapp.User
    """
    # authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserCreateUpdateSerializers

    def post(self, request, *args, **kwargs):

        try:
            return super().post(request, *args, **kwargs)
        except Exception as ex:
            return response.Response({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API Endpoint for update users of authapp.User
    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserCreateUpdateSerializers
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class StudentsListApiView(generics.ListAPIView):
    # authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserSerializers

    def get_queryset(self):
        params = QueryParams(self.request.GET)
        return Filter.user_filter(params)


class StudentStatusUpdateApiView(generics.UpdateAPIView):
    """
    API Endpoint for update only student status
    """

    # authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = StudentStatusSerializers
    queryset = User.objects.all()


# subscription
class StudentDetailApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserDetailSerializers
    queryset = User.objects.all()


class SubscriptionPaginateListApiView(generics.ListAPIView):
    # authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = SubscriptionListSerializers
    pagination_class = StandardResultsSetPagination
    queryset = StudentSubscription.objects.all()

    def get(self, request, *args, **kwargs):
        params = QueryParams(request.GET)

        if not params.all:
            self.pagination_class.page_size = params.perPage
        else:
            self.pagination_class.page_size = StudentSubscription.objects.count()

        return super().get(request, *args, **kwargs)


class SubscriptionListApiView(generics.ListAPIView):
    # authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = SubscriptionListSerializers
    queryset = StudentSubscription.objects.all()


class SubscriptionUpdateApiView(generics.UpdateAPIView):
    # authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = SubscriptionListSerializers
    queryset = StudentSubscription.objects.all()


class SubscriptionCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = SubscriptionListSerializers


# manger
class ManagerListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = ManagerListSerializers
    queryset = User.objects.filter(is_staff=True)


# teacher
class TeacherListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = TeacherListSerializers
    queryset = User.objects.filter(is_teacher=True)

    def get_queryset(self):
        queryset = super().get_queryset()

        if any([*self.request.GET.values()]):
            params = TeacherQueryParams(self.request.GET)
            return Filter.free_teacher_filter(queryset=queryset, params=params)

        return queryset


#schedule
class ScheduleCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = ScheduleCreateSerializers


class ScheduleExistGroupCreateApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def post(self, requset: HttpRequest, **kwargs):
        try:
            data = loads(requset.body.decode('utf-8')) # {"group":27,"user":75}
            group = Group.objects.get(pk=data.get('group'))
            group.students.add(User.objects.get(pk=data.get('user')))
            group.save()

            return Response({'ok': True, 'message': 'ok'}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'ok': False, 'message': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ScheduleDestroyApiView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = ScheduleCreateSerializers
    queryset = Schedule


class ScheduleGroupCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = ScheduleGroupCreateSerializers



# group
class GroupListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = GroupSerializer
    queryset = Group.objects.filter(
        Q(status__in=[Group.STATUS_LEARN, Group.STATUS_OPEN]) &
        ~Q(title__contains='IND') & ~Q(title__contains='user')
        )

    def get_queryset(self):
        queryset = super().get_queryset()

        if any([*self.request.GET.values()]):
            params = TeacherQueryParams(self.request.GET)
            return Filter.group_filter(queryset=queryset, params=params)

        return queryset


class GroupDeleteUserDelteApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def post(self, requset: HttpRequest, **kwargs):
        try:
            data = loads(requset.body.decode('utf-8'))
            group = Group.objects.get(pk=data.get('group'))
            group.students.remove(User.objects.get(pk=data.get('user')))
            group.save()

            return Response({'ok': True, 'message': 'ok'}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'ok': False, 'message': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


# utils
class SubjectListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = SubjectListSerializers
    queryset = Subject.objects.all()