# Generated by Django 4.0.1 on 2022-02-15 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0009_alter_voximplantrecordlesson_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='record',
        ),
        migrations.AddField(
            model_name='voximplantrecordlesson',
            name='record',
            field=models.TextField(blank=True),
        ),
    ]
