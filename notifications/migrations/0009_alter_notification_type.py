# Generated by Django 4.0.1 on 2022-02-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_notification_lesson_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(blank=True, choices=[('LSN_SCH', 'Урок назначен'), ('LSN_CMN', 'Урок скоро состоится'), ('LSN_PRG', 'Урок идет'), ('LSN_DN', 'Урок проведен'), ('LSN_REQ_RESCH', 'Запрос на перенос урока'), ('LSN_REQ_CNL', 'Запрос на отмену урока'), ('LSN_RESCH', 'Урок перенесен'), ('LSN_CNL', 'Урок отменен')], max_length=20, null=True, verbose_name='Тип уведомления'),
        ),
    ]
