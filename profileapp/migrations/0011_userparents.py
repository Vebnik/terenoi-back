# Generated by Django 4.0.1 on 2022-03-09 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profileapp', '0010_subject_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserParents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='ФИО Родителя')),
                ('parent_phone', models.CharField(blank=True, max_length=25, null=True, verbose_name='Телефон родителя')),
                ('parent_email', models.CharField(blank=True, max_length=100, null=True, verbose_name='Email родителя')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Родитель',
                'verbose_name_plural': 'Родители',
            },
        ),
    ]
