# Generated by Django 4.0 on 2022-01-08 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_remove_service_body_service_capacity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.TextField(blank=True, max_length=150),
        ),
    ]
