# Generated by Django 4.0.1 on 2022-04-23 22:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AmoCRM', '0009_clients_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь Terenoi'),
        ),
    ]
