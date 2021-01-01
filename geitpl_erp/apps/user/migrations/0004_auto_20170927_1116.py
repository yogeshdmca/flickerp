# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 11:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customuser_notice_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to=settings.AUTH_USER_MODEL),
        ),
    ]