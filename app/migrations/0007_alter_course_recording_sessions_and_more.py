# Generated by Django 5.0.6 on 2024-07-23 06:59

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_course_starting_date_alter_installment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='recording_sessions',
            field=models.ManyToManyField(blank=True, null=True, to='app.sessions'),
        ),
        migrations.AlterField(
            model_name='course',
            name='starting_date',
            field=models.DateField(default=datetime.datetime(2024, 7, 23, 6, 59, 47, 796655, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, related_name='students', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='installment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 23, 6, 59, 47, 798655, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 23, 6, 59, 47, 796655, tzinfo=datetime.timezone.utc)),
        ),
    ]
