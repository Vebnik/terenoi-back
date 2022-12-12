# Generated by Django 4.0.1 on 2022-04-04 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0015_homeworknotification_lesson_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeworknotification',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата оплаты'),
        ),
        migrations.AddField(
            model_name='lessonratenotification',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата оплаты'),
        ),
        migrations.AddField(
            model_name='notification',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата оплаты'),
        ),
        migrations.AddField(
            model_name='paymentnotification',
            name='lesson_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата урока'),
        ),
        migrations.AddField(
            model_name='paymentnotification',
            name='lesson_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Номер урока'),
        ),
        migrations.AlterField(
            model_name='homeworknotification',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Уведомлениe пользователя'),
        ),
        migrations.AlterField(
            model_name='lessonratenotification',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Уведомлениe пользователя'),
        ),
    ]