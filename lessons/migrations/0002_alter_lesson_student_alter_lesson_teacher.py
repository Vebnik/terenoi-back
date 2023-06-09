# Generated by Django 4.0.1 on 2022-01-20 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='student',
            field=models.ForeignKey(limit_choices_to={'role': 'ST'}, on_delete=django.db.models.deletion.CASCADE, related_name='lesson_student', to=settings.AUTH_USER_MODEL, verbose_name='Ученик'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(limit_choices_to={'role': 'TH'}, on_delete=django.db.models.deletion.CASCADE, related_name='lesson_teacher', to=settings.AUTH_USER_MODEL, verbose_name='Учитель'),
        ),
    ]
