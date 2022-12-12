# Generated by Django 4.0.1 on 2022-03-21 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0008_rename_full_name_teacherbankdata_full_teacher_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherbankdata',
            name='bik',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='БИК'),
        ),
        migrations.AlterField(
            model_name='teacherbankdata',
            name='bill',
            field=models.CharField(max_length=255, verbose_name='Счет получателя'),
        ),
    ]