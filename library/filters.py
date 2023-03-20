from django_filters import rest_framework as filters
from library.models import Resource


class ResourceFilter(filters.FilterSet):
    language = filters.NumberFilter(field_name='language__id')
    level = filters.AllValuesMultipleFilter(field_name='level_language__id')
    section = filters.AllValuesMultipleFilter(field_name='section__id')

    class Meta:
        model = Resource
        fields = ['language', 'level', 'section']
