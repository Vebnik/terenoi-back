# Generated by Django 4.0.1 on 2022-03-22 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0018_remove_user_language_userstudylanguage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userstudylanguage',
            options={'verbose_name': 'Язык обучения пользователя', 'verbose_name_plural': 'Языки обучения пользователей'},
        ),
    ]
