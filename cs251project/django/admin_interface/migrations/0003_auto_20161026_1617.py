# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0002_auto_20161026_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('rollno', models.CharField(max_length=15, primary_key=True, serialize=False)),
            ],
        ),
        migrations.RenameField(
            model_name='instructor',
            old_name='gmail_fb_login',
            new_name='google_fb_login',
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='admin_interface.Student'),
        ),
    ]
