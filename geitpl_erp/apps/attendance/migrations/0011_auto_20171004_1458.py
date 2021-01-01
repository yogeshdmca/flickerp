# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0010_auto_20171004_0703'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='reject_type',
            field=models.CharField(choices=[('1', 'A1'), ('2', 'A2'), ('3', 'A3')], default='1', max_length=25),
        ),
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(choices=[('0', 'Waiting for approval'), ('1', 'Approved'), ('2', 'Reject'), ('3', 'A2'), ('4', 'A3')], default='0', max_length=25),
        ),
    ]