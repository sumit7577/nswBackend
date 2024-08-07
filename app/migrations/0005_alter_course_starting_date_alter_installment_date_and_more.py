# Generated by Django 5.0.6 on 2024-07-23 05:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_sessions_rename_price_course_registration_fees_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='starting_date',
            field=models.DateField(default=datetime.datetime(2024, 7, 23, 5, 36, 37, 213796, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='installment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 23, 5, 36, 37, 215796, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 23, 5, 36, 37, 213796, tzinfo=datetime.timezone.utc)),
        ),
    ]
