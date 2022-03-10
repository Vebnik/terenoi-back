# Generated by Django 4.0.1 on 2022-03-09 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profileapp', '0012_alter_userparents_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalUserPurpose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(max_length=255, verbose_name='Цель')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileapp.subject', verbose_name='Предмет')),
                ('user', models.ForeignKey(limit_choices_to={'is_student': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
