# Generated by Django 2.2 on 2019-05-17 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20190517_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='class_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.ClassTeam'),
        ),
    ]
