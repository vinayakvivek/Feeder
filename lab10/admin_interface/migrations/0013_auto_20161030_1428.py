# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 08:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_interface', '0012_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='id',
        ),
        migrations.AddField(
            model_name='instructor',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]