# Generated by Django 4.0.1 on 2022-11-04 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0033_remove_teacherworkhours_end_time_and_more'),
        ('authapp', '0030_pruffmeaccount_webinar'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinar',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson'),
        ),
    ]
