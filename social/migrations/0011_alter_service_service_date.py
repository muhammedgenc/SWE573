# Generated by Django 4.0 on 2022-01-09 06:15

import datetime
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_rename_applicationdate_serviceapplication_application_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_date',
            field=models.DateField(default=django.utils.timezone.now, validators=[django.core.validators.MinValueValidator(datetime.date(2022, 1, 9))]),
        ),
    ]
