# Generated by Django 4.0.1 on 2022-03-24 19:28
import json
import os

from django.db import migrations

JSON_PATH = 'profileapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


def forwards_func(apps, schema_editor):
    subjects = apps.get_model('profileapp', 'Subject')
    subjects_json = load_from_json('subjects')
    for sb in subjects_json:
        subjects.objects.create(**sb)


class Migration(migrations.Migration):
    dependencies = [
        ('profileapp', '0025_alter_teacheragelearning_options'),
    ]

    operations = [
        migrations.RunPython(code=forwards_func)
    ]