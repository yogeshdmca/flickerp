# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2020-12-01 02:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0041_auto_20201201_0039'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Un paid'), (2, 'Casual Leave'), (3, 'SOL'), (4, 'Medical'), (5, 'Optional'), (6, 'Menstrual')])),
                ('total', models.FloatField(verbose_name='total Leave in year')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaveconf', to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaveconf', to='config.Year')),
            ],
        ),
        migrations.RemoveField(
            model_name='leavebank',
            name='user',
        ),
        migrations.RenameField(
            model_name='leave',
            old_name='request_date',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='leave',
            name='leave_count',
            field=models.FloatField(choices=[(1, 'Full Day'), (0.5, 'Half Day'), (0.25, '2 hours')], default=1, max_length=25),
        ),
        migrations.AddField(
            model_name='leave',
            name='manager',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='leaves_approval', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leave',
            name='shift',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leave', to='attendance.EmployeeShift'),
        ),
        migrations.AddField(
            model_name='leave',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending Approval by TL'), (2, 'Pending Approval by Manager'), (3, 'Approved'), (4, 'Rejected'), (5, 'Rejected with A2'), (6, 'Rejected with A3')], default=1, max_length=25),
        ),
        migrations.AlterField(
            model_name='leave',
            name='description',
            field=models.TextField(verbose_name='Leave Details'),
        ),
        migrations.AlterField(
            model_name='workfromhome',
            name='status',
            field=models.CharField(choices=[('1', 'pending'), ('2', 'Acepted'), ('3', 'Rejected')], default='1', max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='leave',
            unique_together=set([]),
        ),
        migrations.DeleteModel(
            name='LeaveBank',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='leave_for',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='management_approval',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='reject_type',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='status_reason',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='supervisor',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='supervisor_approval',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='time',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='type',
        ),
        migrations.AddField(
            model_name='leave',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leave', to='attendance.LeaveCategory'),
        ),
    ]
