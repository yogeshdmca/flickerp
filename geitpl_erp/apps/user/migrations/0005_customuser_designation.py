# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20170927_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
