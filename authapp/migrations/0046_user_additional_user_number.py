# Generated by Django 4.0.1 on 2023-02-03 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0045_remove_user_additional_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='additional_user_number',
            field=models.ManyToManyField(blank=True, null=True, to='authapp.AdditionalUserNumber', verbose_name='Дополнительный номер'),
        ),
    ]
