# Generated by Django 4.0.1 on 2022-04-21 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AmoCRM', '0004_rename_id_amo_funnel_status_customerstatus_id_amo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerstatus',
            name='funnel',
        ),
    ]
