# Generated by Django 4.0.1 on 2022-03-12 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0008_alter_usercity_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeekDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('number', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Номер дня')),
            ],
            options={
                'verbose_name': 'День недели',
                'verbose_name_plural': 'Дни недели',
            },
        ),
    ]
