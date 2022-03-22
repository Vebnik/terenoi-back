# Generated by Django 4.0.1 on 2022-03-22 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_historypaymentteacher_is_enrollment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherbankdata',
            name='bill',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Счет получателя'),
        ),
        migrations.AlterField(
            model_name='teacherbankdata',
            name='full_teacher_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Получатель'),
        ),
    ]
