# Generated by Django 4.0.1 on 2022-03-30 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0011_alter_usercity_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralContacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=25, null=True, verbose_name='Телефон')),
                ('telegram', models.CharField(blank=True, max_length=255, null=True, verbose_name='Telegram')),
                ('whatsapp', models.CharField(blank=True, max_length=255, null=True, verbose_name='Whatsapp')),
            ],
            options={
                'verbose_name': 'Общие данные для связи',
                'verbose_name_plural': 'Общие данные для связи',
            },
        ),
    ]