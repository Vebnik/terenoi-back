# Generated by Django 4.0.1 on 2022-12-07 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0035_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='crm_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]