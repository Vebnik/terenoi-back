# Generated by Django 4.0.1 on 2023-02-09 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0043_alter_schedule_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='lesson_duration',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Длительность урока, мин'),
        ),
    ]