# Generated by Django 2.2 on 2019-05-19 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20190519_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='own',
        ),
    ]
