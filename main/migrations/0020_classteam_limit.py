# Generated by Django 2.2 on 2019-05-28 18:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20190519_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='classteam',
            name='limit',
            field=models.PositiveSmallIntegerField(default=15, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(5)]),
        ),
    ]
