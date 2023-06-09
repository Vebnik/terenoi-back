# Generated by Django 4.0.1 on 2023-03-06 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0032_alter_userparents_full_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
            ],
            options={
                'verbose_name': 'Специализация учителя',
                'verbose_name_plural': 'Специализации учителя',
            },
        ),
        migrations.CreateModel(
            name='SpecializationItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Пункт')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileapp.specialization', verbose_name='Специализация')),
            ],
            options={
                'verbose_name': 'Пункт специализация учителя',
                'verbose_name_plural': 'Пункты специализации учителя',
            },
        ),
    ]
