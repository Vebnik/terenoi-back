# Generated by Django 4.0.1 on 2022-01-31 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_remove_notification_notification_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='lesson_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата урока'),
        ),
    ]
