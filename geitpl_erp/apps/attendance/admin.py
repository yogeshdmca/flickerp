from django.contrib import admin
from .models import *


class LeaveCategoryTabularAdmin(admin.TabularInline):
    model = LeaveCategory
    fields = ('type', 'total','year')
    readonly_fields=('available',)


class UserAttendanceLogSummaryInline(admin.TabularInline):
    model = UserAttendanceLogSummary


class UserAttendanceLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']
    ordering = ['date']
    inlines = [
        UserAttendanceLogSummaryInline,
    ]

class LeaveAdmin(admin.ModelAdmin):
    list_display = ['user','date',"category", "get_status_display"]
    ordering = ['date']
    list_filter=('user',)

class HolidaysAdmin(admin.ModelAdmin):
    list_display = ['date', 'end_date','type','description']
    ordering = ['date']


class LeaveCategoryAdmin(admin.ModelAdmin):
    list_display = ['type','total','user','year','available']
    ordering = ['user']
    search_fields = ['user__first_nam', 'type','year']
    list_filter = ('user', 'type','year')



class ShiftAdmin(admin.ModelAdmin):
    list_display = ['user','date', 'shift']
    ordering = ['-date']
    list_filter=('user','date')


class ShiftCongAdmin(admin.ModelAdmin):
    list_display = ['time_from','time_to', 'shift_type','is_active']
    ordering = ['-time_from',]
    list_filter=('is_active',)


class WorkFromHomeAdmin(admin.ModelAdmin):
    list_display = ['user','date', 'status','supervisor']
    ordering = ['-date',]
    list_filter=('status','supervisor')

# Register your models here.

admin.site.register(AttendanceMachineLog)

admin.site.register(UserAttendanceLog,UserAttendanceLogAdmin)
admin.site.register(UserAttendanceLogSummary)
admin.site.register(Leave,LeaveAdmin)

admin.site.register(Holidays,HolidaysAdmin)
admin.site.register(LeaveCategory,LeaveCategoryAdmin)

admin.site.register(EmployeeShift,ShiftAdmin)
admin.site.register(Shift,ShiftCongAdmin)

admin.site.register(WorkFromHome,WorkFromHomeAdmin)

admin.site.register(HubstaffUser)