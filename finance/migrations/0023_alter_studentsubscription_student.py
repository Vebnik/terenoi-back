# Generated by Django 4.0.1 on 2023-02-23 19:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0022_alter_studentsubscription_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsubscription',
            name='student',
            field=models.ManyToManyField(blank=True, related_name='subscription_students', to=settings.AUTH_USER_MODEL),
        ),
    ]
