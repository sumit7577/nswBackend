# Generated by Django 5.0.6 on 2024-08-28 06:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_course_course_mode_alter_course_batch_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='content',
            field=models.TextField(default='', max_length=10000, verbose_name='Course Content'),
        ),
        migrations.AlterField(
            model_name='course',
            name='starting_date',
            field=models.DateField(default=datetime.datetime(2024, 8, 28, 6, 48, 32, 663010, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='course',
            name='teaching_time_end',
            field=models.TimeField(blank=True, null=True, verbose_name='Session Time End'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teaching_time_start',
            field=models.TimeField(blank=True, null=True, verbose_name='Session Time Start'),
        ),
        migrations.AlterField(
            model_name='installment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 28, 6, 48, 32, 665011, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 28, 6, 48, 32, 662011, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 28, 6, 48, 32, 663010, tzinfo=datetime.timezone.utc)),
        ),
    ]