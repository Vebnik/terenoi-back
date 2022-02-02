# Generated by Django 4.0.1 on 2022-02-02 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0004_alter_subject_user'),
        ('lessons', '0006_alter_lesson_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(blank=True, limit_choices_to={'user': models.ForeignKey(limit_choices_to={'is_teacher': True}, on_delete=django.db.models.deletion.CASCADE, related_name='lesson_teacher', to=settings.AUTH_USER_MODEL, verbose_name='Учитель')}, null=True, on_delete=django.db.models.deletion.CASCADE, to='profileapp.subject', verbose_name='Предмет'),
        ),
    ]
