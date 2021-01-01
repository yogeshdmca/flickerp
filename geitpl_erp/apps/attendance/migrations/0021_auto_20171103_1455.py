# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-03 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0020_auto_20171012_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='management_approval',
            field=models.CharField(choices=[('0', 'Waiting for management approval'), ('1', 'Approved'), ('2', 'Rejected')], default='0', max_length=25),
        ),
        migrations.AlterField(
            model_name='leave',
            name='supervisor_approval',
            field=models.CharField(choices=[('0', 'Waiting for supervisor approval'), ('1', 'Approved'), ('2', 'Rejected')], default='0', max_length=25),
        ),
    ]