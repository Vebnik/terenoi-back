# Generated by Django 4.0.1 on 2022-11-03 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0026_webinar'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinar',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время и дата начала урока'),
        ),
    ]
