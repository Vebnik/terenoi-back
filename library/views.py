from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import User
from library.filters import ResourceFilter
from library.models import Section, Resource, ResourceLikeList, ResourceFavoriteList
from library.serializers import AllSectionSerializer, ResourcesSerializer, ResourceItemSerializer, AdvicesSerializer, \
    AdviceItemSerializer, SectionResourceSerializer


class AllSectionListView(generics.ListAPIView):
    """Список всех разделов"""
    permission_classes = [IsAuthenticated]
    serializer_class = AllSectionSerializer
    queryset = Section.objects.filter(parent_section=None)


class ResourcesListView(viewsets.ReadOnlyModelViewSet):
    """Список всех курсов"""
    permission_classes = [IsAuthenticated]
    serializer_class = ResourcesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ResourceFilter

    def get_queryset(self):
        return Resource.objects.filter(section__parent_section=self.kwargs.get('pk'), is_advice=False)

    @action(detail=False, methods=['GET'])
    def grouped_by_section(self, request, pk):
        queryset = self.filter_queryset(self.get_queryset())
        result = []
        Section.objects.filter(parent_section=pk)
        sections = Section.objects.filter(parent_section=pk)
        for item in sections:
            resources_list = [res for res in queryset if res.section == item]
            serializer_section = SectionResourceSerializer(item)
            serializer = self.get_serializer(resources_list, many=True)
            data = {'section': serializer_section.data, 'resources': serializer.data}
            result.append(data)
        return Response(result)


class FavoriteResourcesListView(viewsets.ReadOnlyModelViewSet):
    """Список всех курсов в избранном"""
    permission_classes = [IsAuthenticated]
    serializer_class = ResourcesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ResourceFilter

    def get_queryset(self):
        favorite_resource = ResourceFavoriteList.objects.filter(user=self.request.user,
                                                                resource__is_advice=False,
                                                                resource__section__parent_section=self.kwargs.get('pk')
                                                                )
        favorite_list = []
        for item in favorite_resource:
            favorite_list.append(item.resource.pk)
        return Resource.objects.filter(pk__in=favorite_list)

    @action(detail=False, methods=['GET'])
    def grouped_by_section(self, request, pk):
        queryset = self.filter_queryset(self.get_queryset())
        result = []
        Section.objects.filter(parent_section=pk)
        sections = Section.objects.filter(parent_section=pk)
        for item in sections:
            resources_list = [res for res in queryset if res.section == item]
            serializer_section = SectionResourceSerializer(item)
            serializer = self.get_serializer(resources_list, many=True)
            data = {'section': serializer_section.data, 'resources': serializer.data}
            result.append(data)
        return Response(result)


class AdvicesListView(generics.ListAPIView):
    """Список всех советов"""
    permission_classes = [IsAuthenticated]
    serializer_class = AdvicesSerializer

    def get_queryset(self):
        return Resource.objects.filter(is_advice=True)


class FavoriteAdvicesListView(generics.ListAPIView):
    """Список всех советов в избранном"""
    permission_classes = [IsAuthenticated]
    serializer_class = AdvicesSerializer

    def get_queryset(self):
        favorite_resource = ResourceFavoriteList.objects.filter(user=self.request.user,
                                                                resource__is_advice=True)
        favorite_list = []
        for item in favorite_resource:
            favorite_list.append(item.resource.pk)
        return Resource.objects.filter(pk__in=favorite_list)


class ResourceItemListView(generics.RetrieveAPIView):
    """Ресурс"""
    permission_classes = [IsAuthenticated]
    serializer_class = ResourceItemSerializer
    queryset = Resource.objects.all()


class AdviceItemListView(generics.RetrieveAPIView):
    """Совет"""
    permission_classes = [IsAuthenticated]
    serializer_class = AdviceItemSerializer
    queryset = Resource.objects.all()


class AddResourceLikeView(APIView):
    """Добавление лайка к ресурсу"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def post(self, request):
        user = self.get_object()
        resource = Resource.objects.filter(pk=self.request.data.get('id')).first()
        if resource:
            ResourceLikeList.objects.create(user=user, resource=resource)
            data = {'message': True}
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            data = {'message': False}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


class DeleteResourceLikeView(APIView):
    """Удаление лайка с ресурса"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def post(self, request):
        user = self.get_object()
        resource = Resource.objects.filter(pk=self.request.data.get('id')).first()
        like = ResourceLikeList.objects.filter(user=user, resource=resource)
        if like:
            like.delete()
            data = {'message': True}
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            data = {'message': False}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


class AddResourceFavoriteListView(APIView):
    """Добавление ресурса в избранное"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def post(self, request):
        user = self.get_object()
        resource = Resource.objects.filter(pk=self.request.data.get('id')).first()
        if resource:
            ResourceFavoriteList.objects.create(user=user, resource=resource)
            data = {'message': True}
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            data = {'message': False}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


class DeleteResourceFavoriteListView(APIView):
    """Удаление ресурса из избраного """
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def post(self, request):
        user = self.get_object()
        resource = Resource.objects.filter(pk=self.request.data.get('id')).first()
        favorite = ResourceFavoriteList.objects.filter(user=user, resource=resource)
        if favorite:
            favorite.delete()
            data = {'message': True}
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            data = {'message': False}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


class FavoriteResourceCountView(APIView):
    """Количество ресурсов в избранном"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request):
        user = self.get_object()
        favorite = ResourceFavoriteList.objects.filter(user=user)
        data = {'count': favorite.count()}
        return Response(data=data, status=status.HTTP_200_OK)
