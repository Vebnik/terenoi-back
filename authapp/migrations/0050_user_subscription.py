# Generated by Django 4.0.1 on 2023-02-08 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0015_studentsubscription_student'),
        ('authapp', '0049_alter_user_is_pass_generation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.studentsubscription'),
        ),
    ]
