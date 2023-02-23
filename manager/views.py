from django.views.generic import TemplateView
from authapp.models import User
from manager.mixins import UserAccessMixin
from manager.service import Utils, StandardResultsSetPagination, QueryParams, Filter
from finance.models import StudentSubscription
from rest_framework import generics, permissions, authentication, status, response

from manager.serializers import (
    UserSerializers, UserCreateUpdateSerializers, 
    UserDetailSerializers, SubscriptionListSerializers
)

class ManagerTemplateView(UserAccessMixin, TemplateView):
    template_name = 'manager/index.html'


class UserListApiView(generics.ListAPIView):
    """
    API Endpoint for get users of authapp.User
    """
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
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


class UserCreateAPIView(generics.CreateAPIView):
    """
    API Endpoint for create users of authapp.User
    """
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserCreateUpdateSerializers

    def post(self, request, *args, **kwargs):

        try:
            return super().post(request, *args, **kwargs)
        except Exception as ex:
            return response.Response({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API Endpoint for update users of authapp.User
    """
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserCreateUpdateSerializers
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UsersListApiView(generics.ListAPIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserSerializers

    def get_queryset(self):
        params = QueryParams(self.request.GET)
        return Filter.user_filter(params)


class UserDetailApiView(generics.RetrieveAPIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = UserDetailSerializers
    queryset = User.objects.all()


class SubscriptionListApiView(generics.ListAPIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = SubscriptionListSerializers
    queryset = StudentSubscription.objects.all()


class SubscriptionUpdateApiView(generics.UpdateAPIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = SubscriptionListSerializers
    queryset = StudentSubscription.objects.all()