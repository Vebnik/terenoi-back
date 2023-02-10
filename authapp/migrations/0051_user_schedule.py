# Generated by Django 4.0.1 on 2023-02-09 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0044_schedule_lesson_duration'),
        ('authapp', '0050_user_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.schedulesettings'),
        ),
    ]
