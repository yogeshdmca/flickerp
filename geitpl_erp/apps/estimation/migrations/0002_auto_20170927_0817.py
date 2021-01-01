# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 08:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estimation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opportunity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimation',
            name='assigned_to',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='estimation',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estimation_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='estimation',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opportunity.Lead'),
        ),
        migrations.AddField(
            model_name='estimation',
            name='modified_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estimation_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
    ]