import json
import os
from django.core.management import BaseCommand
from profileapp.models import GlobalPurpose, Subject

JSON_PATH = 'profileapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **options):
        purposes = load_from_json('purpose')
        GlobalPurpose.objects.all().delete()
        for prp in purposes:
            subject_name = prp['subject']
            subject_item = Subject.objects.filter(name=subject_name).first()
            prp['subject'] = subject_item
            GlobalPurpose.objects.create(**prp)
