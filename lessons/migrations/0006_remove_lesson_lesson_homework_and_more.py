# Generated by Django 4.0.1 on 2022-02-06 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0005_lesson_lesson_homework_lesson_lesson_materials_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='lesson_homework',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='lesson_materials',
        ),
        migrations.CreateModel(
            name='LessonMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.FileField(blank=True, null=True, upload_to='materials-for-lesson/', verbose_name='Материалы к уроку')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson', verbose_name='Урок')),
            ],
            options={
                'verbose_name': 'Материал к уроку',
                'verbose_name_plural': 'Материалы к уроку',
            },
        ),
        migrations.CreateModel(
            name='LessonHomework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homework', models.FileField(blank=True, null=True, upload_to='homework-for-lesson/', verbose_name='Домашнее задание к уроку')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson', verbose_name='Урок')),
            ],
            options={
                'verbose_name': 'Домашнее задание к уроку',
                'verbose_name_plural': 'Домашнее задание к уроку',
            },
        ),
    ]
