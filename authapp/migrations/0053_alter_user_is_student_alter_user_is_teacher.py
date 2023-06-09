# Generated by Django 4.0.1 on 2023-02-14 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0052_alter_additionalusernumber_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_student',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Ученик'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_teacher',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Учитель'),
        ),
    ]
