# Generated by Django 2.2 on 2019-05-13 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190513_0436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='student',
        ),
        migrations.AddField(
            model_name='student',
            name='ratings',
            field=models.ManyToManyField(to='main.Rating'),
        ),
    ]
