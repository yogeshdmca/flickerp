# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_auto_20171004_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='reject_type',
            field=models.CharField(blank=True, choices=[('1', 'A1'), ('2', 'A2'), ('3', 'A3')], default='1', max_length=25, null=True),
        ),
    ]