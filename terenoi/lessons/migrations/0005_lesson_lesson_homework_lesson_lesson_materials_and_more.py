# Generated by Django 4.0.1 on 2022-02-02 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0005_remove_subject_subject_remove_subject_user_and_more'),
        ('lessons', '0004_alter_lesson_student_alter_lesson_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_homework',
            field=models.FileField(blank=True, null=True, upload_to='homework-for-lesson/', verbose_name='Домашнее задание к уроку'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_materials',
            field=models.FileField(blank=True, null=True, upload_to='materials-for-lesson/', verbose_name='Материалы к уроку'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profileapp.subject', verbose_name='Предмет'),
        ),
    ]
