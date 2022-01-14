# Generated by Django 4.0.1 on 2022-01-11 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_user_phone_alter_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='education',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Образование'),
        ),
        migrations.AddField(
            model_name='user',
            name='experience',
            field=models.TextField(blank=True, null=True, verbose_name='Опыт работы'),
        ),
        migrations.AddField(
            model_name='user',
            name='subject',
            field=models.CharField(choices=[('EN', 'Английский')], default='EN', max_length=3, verbose_name='Предмет'),
        ),
    ]
