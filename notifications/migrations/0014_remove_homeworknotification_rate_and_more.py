# Generated by Django 4.0.1 on 2022-03-31 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0013_alter_managernotification_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homeworknotification',
            name='rate',
        ),
        migrations.AddField(
            model_name='managernotification',
            name='lesson_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Номер урока'),
        ),
        migrations.AddField(
            model_name='managernotification',
            name='to_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_notification', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь,который поставил оценку к уроку'),
        ),
        migrations.AlterField(
            model_name='homeworknotification',
            name='type',
            field=models.CharField(blank=True, choices=[('HM_ADD', 'Домашнее задание добавлено'), ('HM_CHK', 'Домашнее задание проверено')], max_length=20, null=True, verbose_name='Тип уведомления'),
        ),
        migrations.AlterField(
            model_name='managernotification',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager_notification', to=settings.AUTH_USER_MODEL, verbose_name='Менежер'),
        ),
        migrations.AlterField(
            model_name='managernotification',
            name='type',
            field=models.CharField(blank=True, choices=[('NU', 'Новый пользователь'), ('REQ_LSN_RESCH', 'Запрос на перенос урока'), ('REQ_LSN_CNL', 'Запрос на отмену урока'), ('REQ_RJC_U', 'Запрос на отказ от ученика'), ('REQ_CHN_PSS', 'Запрос на смену пароля'), ('LESS_RT_HGH', 'Оценка за урок не удовлетворительная'), ('LESS_RT_HGH', 'Оценка за урок высокая')], max_length=20, null=True, verbose_name='Тип уведомления'),
        ),
        migrations.CreateModel(
            name='LessonRateNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_id', models.IntegerField(blank=True, null=True, verbose_name='Номер урока')),
                ('type', models.CharField(blank=True, choices=[('LESS_RT_HGH', 'Урок оценен высоко'), ('LESS_RT_HGH', 'Урок оценен не удовлетворительно')], max_length=20, null=True, verbose_name='Тип уведомления')),
                ('is_read', models.BooleanField(default=False, verbose_name='Просмотрено')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Уведомление по оценке урока',
                'verbose_name_plural': 'Уведомления по оценке урока',
            },
        ),
    ]
