# Generated by Django 4.0.1 on 2022-11-03 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0025_user_alfa_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webinar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Автоматическое название')),
                ('hash', models.CharField(blank=True, max_length=255, null=True, verbose_name='Хэш')),
            ],
        ),
    ]
