# Generated by Django 4.0.1 on 2022-04-01 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0014_remove_homeworknotification_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeworknotification',
            name='lesson_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата урока'),
        ),
        migrations.AddField(
            model_name='homeworknotification',
            name='message',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Сообщение'),
        ),
        migrations.AddField(
            model_name='lessonratenotification',
            name='lesson_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата урока'),
        ),
        migrations.AddField(
            model_name='lessonratenotification',
            name='message',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Сообщение'),
        ),
    ]
