# Generated by Django 4.0.1 on 2022-02-25 23:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0016_alter_managerrequests_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerrequests',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата урока'),
        ),
        migrations.AlterField(
            model_name='managerrequests',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]