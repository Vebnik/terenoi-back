# Generated by Django 4.0.1 on 2022-03-12 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0017_alter_userinterest_options'),
        ('lessons', '0020_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profileapp.subject', verbose_name='Предмет'),
        ),
    ]
