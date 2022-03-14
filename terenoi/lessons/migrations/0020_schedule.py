# Generated by Django 4.0.1 on 2022-03-12 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0009_weekdays'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0019_alter_managerrequests_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='Время')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название')),
                ('near_meet', models.DateTimeField(blank=True, null=True, verbose_name='Ближайший урок')),
                ('finished', models.BooleanField(default=False, verbose_name='Расписание завершено')),
                ('student', models.ForeignKey(limit_choices_to={'is_student': True}, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_student', to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
                ('teacher', models.ForeignKey(limit_choices_to={'is_teacher': True}, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_teacher', to=settings.AUTH_USER_MODEL, verbose_name='Учитель')),
                ('weekday', models.ManyToManyField(to='settings.WeekDays', verbose_name='Дни недели')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписания',
            },
        ),
    ]
