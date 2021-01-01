# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models


@admin.register(models.TimesheetType)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ("title", "type", "developer", "supervisore")

    search_fields = ("title", "type", "developer", "supervisore")


class ServiceRecordsInLine(admin.TabularInline):
    model = models.ServiceRecords
    extra = 0


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = ("title", "type", "status",
                    "assigned_to", "parent")

    search_fields = ["title", "type", "status"]
    list_filter = ("type",'status',)

    inlines = [
        ServiceRecordsInLine
    ]

    def renew_count(self, obj):
        return obj.records.all().count()


@admin.register(models.ScheduleAllotment)
class ScheduleAllotmentAdmin(admin.ModelAdmin):

    list_display = ("service", "alloted_to", "hours", "date")


# class ServiceAllotmentInLine(admin.TabularInline):
#     model = models.DailyServiceAllotment
#     extra = 0

# class TimesheetFiledInLine(admin.TabularInline):
#     model = models.TimesheetFiled
#     extra = 0


# @admin.register(models.ServiceRecords)
# class ServiceAdmin(admin.ModelAdmin):

#     list_display = ("service", "title","start_date","end_date")

#     search_fields = ["title", "start_date"]

#     inlines = [
#         ServiceAllotmentInLine,TimesheetFiledInLine
#     ]


@admin.register(models.TimesheetFiled)
class TimesheetAdmin(admin.ModelAdmin):

    list_display = ("category", "date", "hours", "service", 'help_to')
