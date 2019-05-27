# Generated by Django 2.2 on 2019-04-09 19:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import main.models
import main.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassNo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_no', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('IT.f', 'February Standard'), ('IT.a', 'August Standard'), ('IT.m', 'May Express'), ('IT.o', 'October Express'), ('IT.s', 'STEM High achievers')], max_length=4)),
                ('year', models.PositiveSmallIntegerField(default=18, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(18)])),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_code', models.CharField(blank=True, max_length=8, null=True)),
                ('password', models.CharField(blank=True, max_length=8, null=True)),
                ('surname', models.CharField(blank=True, max_length=75, null=True)),
                ('given_name', models.CharField(blank=True, max_length=50, null=True)),
                ('pref_name', models.CharField(blank=True, max_length=25, null=True)),
                ('email', models.EmailField(blank=True, max_length=70, null=True)),
                ('class_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ClassNo')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Group')),
            ],
        ),
        migrations.CreateModel(
            name='CSVUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=main.models.upload_csv_file, validators=[main.validators.csv_file_validator])),
                ('completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='classno',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Group'),
        ),
    ]
