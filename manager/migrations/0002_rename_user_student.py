# Generated by Django 4.0.1 on 2023-01-19 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Student',
        ),
    ]