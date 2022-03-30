from rest_framework import serializers

from authapp.models import User
from settings.models import CityTimeZone, UserCity, GeneralContacts


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


class CityUserSerializer(serializers.ModelSerializer):
    city_title = serializers.SerializerMethodField()

    class Meta:
        model = UserCity
        fields = ('city_title',)

    def get_city_title(self, instance):
        city = CityTimeZone.objects.filter(city=instance.city).first()
        if not city:
            return None
        return city.city


class GeneralContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralContacts
        fields = ('phone', 'telegram', 'whatsapp')
