# Generated by Django 4.0.1 on 2022-03-14 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0023_remove_schedule_count_remove_schedule_finished_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedulesettings',
            old_name='near_meet',
            new_name='near_lesson',
        ),
        migrations.AddField(
            model_name='schedulesettings',
            name='last_lesson',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Последний урок'),
        ),
    ]
