# Generated by Django 4.0.1 on 2022-03-29 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0021_user_telegram_user_whatsapp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_pass_generation',
            field=models.BooleanField(default=False, verbose_name='Сгенерировать пароль'),
        ),
    ]
