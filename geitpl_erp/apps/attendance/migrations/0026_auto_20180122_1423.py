# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-22 08:53
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0025_remove_leavebank_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='leave_for',
            field=models.CharField(choices=[(b'8', b'Full Day(9 hrs)'), (b'6.5', b'3/4 day (6 hrs 45 min)'), (b'5', b'1/2 day (4 hrs 30 min)'), (b'2.5', b'1/4 day (2 hrs 15 min)'), (b'1', b'1 Hour')], default=b'8', max_length=10),
        ),
        migrations.AddField(
            model_name='leave',
            name='request_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leave',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leaves_approval', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leave',
            name='time',
            field=models.TimeField(blank=True, choices=[(datetime.time(10, 0), b'10:00 AM'), (datetime.time(10, 30), b'10:30 AM'), (datetime.time(11, 0), b'11:00 AM'), (datetime.time(11, 30), b'11:30 AM'), (datetime.time(12, 0), b'12:00 PM'), (datetime.time(12, 30), b'12:30 PM'), (datetime.time(13, 0), b'13:00 PM'), (datetime.time(13, 30), b'13:30 PM'), (datetime.time(14, 0), b'14:00 PM'), (datetime.time(14, 30), b'14:30 PM'), (datetime.time(15, 0), b'15:00 PM'), (datetime.time(15, 30), b'15:30 PM'), (datetime.time(16, 0), b'16:00 PM'), (datetime.time(16, 30), b'16:30 PM'), (datetime.time(17, 0), b'17:00 PM'), (datetime.time(17, 30), b'17:30 PM'), (datetime.time(18, 0), b'18:00 PM'), (datetime.time(18, 30), b'18:30 PM'), (datetime.time(19, 0), b'19:00 PM'), (datetime.time(19, 30), b'19:30 PM')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='holidays',
            name='type',
            field=models.CharField(choices=[(b'1', b'Holiday'), (b'2', b'WeekOff'), (b'3', b'Optional')], max_length=10),
        ),
        migrations.AlterField(
            model_name='leave',
            name='type',
            field=models.CharField(choices=[(b'1', b'Casual Leave'), (b'3', b'Emergency Leave'), (b'2', b'Optional')], max_length=10),
        ),
        migrations.AlterField(
            model_name='leave',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='leave',
            unique_together=set([('date', 'user', 'end_date')]),
        ),
    ]
