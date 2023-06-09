# Generated by Django 4.0.1 on 2022-02-18 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profileapp', '0007_referralpromo_from_user_alter_referralpromo_user'),
        ('lessons', '0013_alter_lessonratehomework_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_balance', models.IntegerField(blank=True, null=True, verbose_name='Баланс')),
                ('currency', models.CharField(choices=[('KZT', 'KZT'), ('USD', 'USD')], default='KZT', max_length=5, verbose_name='Валюта')),
                ('bonus_money_balance', models.IntegerField(blank=True, null=True, verbose_name='Бонусный баланс')),
                ('withdrawal_money', models.IntegerField(blank=True, null=True, verbose_name='Выведенные деньги')),
                ('user', models.ForeignKey(limit_choices_to={'is_teacher': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Учитель')),
            ],
            options={
                'verbose_name': 'Баланс учителя',
                'verbose_name_plural': 'Баланс учителя',
            },
        ),
        migrations.CreateModel(
            name='StudentBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_balance', models.IntegerField(blank=True, null=True, verbose_name='Баланс')),
                ('currency', models.CharField(choices=[('KZT', 'KZT'), ('USD', 'USD')], default='KZT', max_length=5, verbose_name='Валюта')),
                ('lessons_balance', models.IntegerField(blank=True, null=True, verbose_name='Баланс уроков')),
                ('bonus_lessons_balance', models.IntegerField(blank=True, null=True, verbose_name='Бонусный баланс уроков')),
                ('user', models.ForeignKey(limit_choices_to={'is_student': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
            ],
            options={
                'verbose_name': 'Баланс ученика',
                'verbose_name_plural': 'Баланс ученика',
            },
        ),
        migrations.CreateModel(
            name='HistoryPaymentTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField(verbose_name='Дата и время зачисления или снятия')),
                ('amount', models.IntegerField(blank=True, null=True, verbose_name='Сумма зачисления или снятия')),
                ('currency', models.CharField(choices=[('KZT', 'KZT'), ('USD', 'USD')], default='KZT', max_length=5, verbose_name='Валюта')),
                ('referral', models.BooleanField(default=False, verbose_name='Реферальная программа')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson', verbose_name='Урок')),
                ('teacher', models.ForeignKey(limit_choices_to={'is_teacher': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Учитель')),
            ],
            options={
                'verbose_name': 'История операций учителя',
                'verbose_name_plural': 'История операций учителя',
            },
        ),
        migrations.CreateModel(
            name='HistoryPaymentStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField(verbose_name='Дата и время зачисления')),
                ('amount', models.IntegerField(blank=True, null=True, verbose_name='Сумма зачисления')),
                ('currency', models.CharField(choices=[('KZT', 'KZT'), ('USD', 'USD')], default='KZT', max_length=5, verbose_name='Валюта')),
                ('lesson_count', models.IntegerField(blank=True, null=True, verbose_name='Кол-во уроков')),
                ('referral', models.BooleanField(default=False, verbose_name='Реферальная программа')),
                ('manager', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL, verbose_name='Менеджер')),
                ('student', models.ForeignKey(limit_choices_to={'is_student': True}, on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profileapp.subject', verbose_name='Предмет')),
            ],
            options={
                'verbose_name': 'История операций ученика',
                'verbose_name_plural': 'История операций ученика',
            },
        ),
    ]
