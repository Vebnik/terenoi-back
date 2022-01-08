from django.shortcuts import render
from rest_framework import generics, permissions
from authapp.models import User
from profileapp.serializers import UpdateUserSerializer


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return User.objects.get(username=self.request.user)