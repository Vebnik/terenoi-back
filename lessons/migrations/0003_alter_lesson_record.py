# Generated by Django 4.0.1 on 2022-01-20 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_alter_lesson_student_alter_lesson_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='record',
            field=models.URLField(blank=True),
        ),
    ]
