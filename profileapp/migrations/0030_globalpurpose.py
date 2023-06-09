# Generated by Django 4.0.1 on 2022-04-01 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0029_remove_globaluserpurpose_purpose'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalPurpose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileapp.subject', verbose_name='Предмет')),
            ],
            options={
                'verbose_name': 'Глобальная цель',
                'verbose_name_plural': 'Глобальные цели',
            },
        ),
    ]
