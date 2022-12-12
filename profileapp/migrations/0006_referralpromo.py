# Generated by Django 4.0.1 on 2022-02-14 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profileapp', '0005_remove_subject_subject_remove_subject_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralPromo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_link', models.CharField(max_length=10, unique=True, verbose_name='Реферальный промо пользователя')),
                ('from_user_link', models.CharField(blank=True, max_length=10, null=True, verbose_name='Реферальный промо друга')),
                ('is_used', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Реферальная программа',
                'verbose_name_plural': 'Реферальная программа',
            },
        ),
    ]