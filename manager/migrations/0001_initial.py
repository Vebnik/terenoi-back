# Generated by Django 4.0.1 on 2023-01-19 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('group', models.CharField(max_length=100)),
                ('ab', models.CharField(max_length=100)),
                ('balance', models.IntegerField(verbose_name='balance')),
                ('status', models.CharField(choices=[('ACT', 'Активный'), ('PAU', 'На паузе'), ('ARC', 'Архивный'), ('CAN', 'Отказ')], default='ACT', max_length=3)),
            ],
        ),
    ]