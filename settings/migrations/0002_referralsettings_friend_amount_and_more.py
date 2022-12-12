# Generated by Django 4.0.1 on 2022-03-02 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralsettings',
            name='friend_amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Сумма выплаты для учителя,которого пригласили'),
        ),
        migrations.AddField(
            model_name='referralsettings',
            name='friend_lesson_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Кол-во уроков для ученика,которого пригласили'),
        ),
    ]