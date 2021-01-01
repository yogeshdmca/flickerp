# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-04 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0006_auto_20171201_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='payslip',
            name='salary_month',
            field=models.CharField(choices=[(b'january', b'January'), (b'feburary', b'Feburary'), (b'march', b'March'), (b'april', b'April'), (b'may', b'May'), (b'june', b'June'), (b'july', b'July'), (b'august', b'August'), (b'september', b'September'), (b'october', b'October'), (b'november', b'November'), (b'december', b'December')], default=b'december', max_length=20),
        ),
        migrations.AddField(
            model_name='payslip',
            name='salary_year',
            field=models.CharField(default=2017, max_length=20),
        ),
    ]