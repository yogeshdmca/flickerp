# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-01 10:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0004_auto_20171202_1044'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='payslip',
            order_with_respect_to='user',
        ),
    ]