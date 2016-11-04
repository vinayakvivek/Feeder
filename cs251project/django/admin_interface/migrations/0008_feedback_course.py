# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0007_auto_20161029_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='course',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='admin_interface.Course'),
            preserve_default=False,
        ),
    ]
