# Generated by Django 4.0.1 on 2022-04-01 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0030_globalpurpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='globaluserpurpose',
            name='purpose',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profileapp.globalpurpose', verbose_name='Цель'),
        ),
    ]
