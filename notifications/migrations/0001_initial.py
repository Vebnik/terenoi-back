# Generated by Django 4.0.1 on 2022-01-27 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(blank=True, choices=[('LSN', 'Обучение')], max_length=3, null=True, verbose_name='Тип уведомления')),
                ('message', models.CharField(blank=True, max_length=255, null=True, verbose_name='Сообщение')),
                ('is_read', models.BooleanField(default=False, verbose_name='Просмотрено')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Уведомлениe пользователя')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
            },
        ),
    ]
