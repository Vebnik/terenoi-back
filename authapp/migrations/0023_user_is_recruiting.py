# Generated by Django 4.0.1 on 2022-04-10 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0022_user_is_pass_generation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_recruiting',
            field=models.BooleanField(default=False, verbose_name='Набор открыт'),
        ),
    ]
