# Generated by Django 4.0.1 on 2022-11-17 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0035_lesson_students_alter_lesson_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='student',
        ),
    ]