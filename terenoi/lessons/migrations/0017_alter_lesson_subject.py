# Generated by Django 4.0.1 on 2022-02-02 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0005_remove_subject_subject_remove_subject_user_and_more'),
        ('lessons', '0016_alter_lesson_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileapp.subject', verbose_name='Предмет'),
        ),
    ]
