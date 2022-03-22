# Generated by Django 4.0.1 on 2022-03-22 01:08
import json
import os

from django.db import migrations

JSON_PATH = 'profileapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


def forwards_func(apps, schema_editor):
    specials = apps.get_model('profileapp', 'MathSpecializations')
    specials_json = load_from_json('math')
    for sp in specials_json:
        specials.objects.create(**sp)


class Migration(migrations.Migration):
    dependencies = [
        ('profileapp', '0021_fill_age'),
    ]

    operations = [
        migrations.RunPython(code=forwards_func)
    ]
