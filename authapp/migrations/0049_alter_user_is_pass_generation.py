# Generated by Django 4.0.1 on 2023-02-08 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0048_alter_user_is_pass_generation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_pass_generation',
            field=models.BooleanField(default=False, verbose_name='Сгенерировать пароль'),
        ),
    ]