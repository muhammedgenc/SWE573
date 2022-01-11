# Generated by Django 4.0 on 2022-01-08 07:29

import datetime
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_service_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='capacity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_date',
            field=models.DateField(default=django.utils.timezone.now, validators=[django.core.validators.MinValueValidator(datetime.date(2022, 1, 8))]),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
