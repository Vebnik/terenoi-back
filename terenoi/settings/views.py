
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import User
from settings.models import CityTimeZone
from settings.serializers import CitiesSerializer


class CitiesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request):
        user = self.get_object()
        serializer = CitiesSerializer(user)
        return Response(serializer.data)
