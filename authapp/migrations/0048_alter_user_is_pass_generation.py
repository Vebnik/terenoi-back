# Generated by Django 4.0.1 on 2023-02-05 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0047_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_pass_generation',
            field=models.BooleanField(default=True, verbose_name='Сгенерировать пароль'),
        ),
    ]
