# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0005_remove_feedback_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.IntegerField(null=True),
        ),
    ]
