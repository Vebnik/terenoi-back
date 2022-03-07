from rest_framework import serializers

from authapp.models import User
from settings.models import CityTimeZone


class CitiesSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    time_zone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('city', 'time_zone')

    def get_city(self, instance):
        cities = CityTimeZone.objects.all().values('city')
        city_lst = []
        for city in cities:
            city_lst.append(city['city'])
        return city_lst

    def get_time_zone(self, instance):
        time_zones = CityTimeZone.objects.all().values('time_zone')
        time_zones_lst = []
        for zone in time_zones:
            time_zones_lst.append(zone['time_zone'])
        return time_zones_lst
