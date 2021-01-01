# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-11 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0011_auto_20190306_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='rating',
            field=models.IntegerField(choices=[(1, '$5 - $8 per hour'), (2, '$8 - $12 per hour'), (3, '$12+ per hour')], default=1, verbose_name='Experience Label Rating'),
        ),
    ]