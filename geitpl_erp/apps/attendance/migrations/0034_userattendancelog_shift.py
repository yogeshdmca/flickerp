# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-02 05:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0033_attendancemachinelog_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='userattendancelog',
            name='shift',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attandance_log', to='attendance.EmployeeShift'),
        ),
    ]
