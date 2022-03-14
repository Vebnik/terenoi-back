# Generated by Django 4.0.1 on 2022-03-14 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0010_fill_weekdays'),
        ('lessons', '0024_rename_near_meet_schedulesettings_near_lesson_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedulesettings',
            name='weekday',
        ),
        migrations.AddField(
            model_name='schedule',
            name='weekday',
            field=models.ManyToManyField(to='settings.WeekDays', verbose_name='Дни недели'),
        ),
    ]
