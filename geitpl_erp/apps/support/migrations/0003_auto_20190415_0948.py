# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-04-15 09:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_industry_portfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to=settings.AUTH_USER_MODEL),
        ),
    ]
