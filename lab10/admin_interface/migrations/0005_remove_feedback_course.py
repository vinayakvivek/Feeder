# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 10:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0004_auto_20161029_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='course',
        ),
    ]
