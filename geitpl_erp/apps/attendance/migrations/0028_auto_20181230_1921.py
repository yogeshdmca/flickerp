# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-30 13:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0027_employeeshift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeshift',
            name='time_from',
            field=models.TimeField(choices=[(datetime.time(8, 0), b'08:00 AM'), (datetime.time(9, 0), b'09:00 AM'), (datetime.time(10, 0), b'10:00 AM'), (datetime.time(11, 0), b'11:00 AM'), (datetime.time(12, 0), b'12:00 PM'), (datetime.time(13, 0), b'13:00 PM'), (datetime.time(14, 0), b'14:00 PM'), (datetime.time(15, 0), b'15:00 PM')], max_length=60, verbose_name=b'Start time'),
        ),
    ]