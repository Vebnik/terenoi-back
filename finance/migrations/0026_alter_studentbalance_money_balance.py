# Generated by Django 4.0.1 on 2023-02-23 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0025_alter_studentbalance_money_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentbalance',
            name='money_balance',
            field=models.IntegerField(default=0, verbose_name='Баланс'),
        ),
    ]
