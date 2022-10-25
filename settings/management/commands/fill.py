import json
import os

from django.core.management import BaseCommand

from settings.models import CityTimeZone

JSON_PATH = 'settings/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **options):
        cities = load_from_json('cities')
        CityTimeZone.objects.all().delete()
        for city in cities:
            CityTimeZone.objects.create(**city)
