from django import template
from attendance.models import UserAttendanceLog, Holidays, Leave
from calendar import monthrange
from datetime import date, datetime, timedelta
from django.db.models import Sum
from user.models import format_timedelta, CustomUser


register = template.Library()

@register.inclusion_tag('users/partials/active_user_select.html')
def active_user_select():
    users = CustomUser.objects.all()
    return {'users':users}


@register.inclusion_tag('users/partials/user_hierarchy_select.html', takes_context=True)
def user_hierarchy_select(context):
    tags = context['request'].user.get_children_for_select_box()
    user_id = context.get('user_id',context['request'].user.id)
    return {'tags':tags, 'current_user':context['request'].user,'user_id':user_id}



@register.inclusion_tag('users/partials/user_hierarchy_select.html', takes_context=True)
def user_hierarchy_select_for_sales(context):
    tags = context['request'].user.get_sales_children_for_select_box()
    return {'tags':tags, 'current_user':context['request'].user}


@register.inclusion_tag('attendance/partials/admin_attendence_list.html')
def get_attendence_for_day(dt,user):
    try:
        day_object = UserAttendanceLog.objects.get(date=dt, user=user)
    except:
        day_object = False

    try:
        holiday = Holidays.objects.get(date__lte=dt, end_date__gte=dt, type='1')
    except:
        try:
            holiday = Holidays.objects.get(date=dt, type='1')
        except:
            holiday = False
    try:
        weekly_off = Holidays.objects.get(date=dt, type='2')
    except:
        weekly_off = False

    try:
        leave = Leave.objects.get(user=user,date__lte=dt, end_date__gte=dt, leave_for='8')
    except:
        try:
            leave = Leave.objects.get(user=user,date=dt,leave_for='8')
        except:
            leave = False

    ctx = {
        'day_object':day_object,
        'weekly_off':weekly_off,
        'holiday':holiday, 
        'leave':leave,
        'dt':dt,
        }
    return ctx


@register.inclusion_tag('attendance/partials/admin_monthly_attendence_list.html')
def get_leaves_and_short_hours(total_working_days, user, month, holidays):
    leave_count = 0
    month_days = monthrange(date.today().year, month)[1]
    month_start_date = date(2017, month, 1)
    month_last_date = date(2017, month, month_days)
    total_days_count = total_working_days

    leaves = Leave.objects.filter(user=user, date__range=(month_start_date, month_last_date))
    for leave in leaves:
        if leave.end_date:
            start_date = leave.date
            while (leave.end_date>=start_date):
                if not holidays.filter(date = start_date).count() > 0:
                    total_days_count = total_days_count-1
                    leave_count += 1
                start_date = start_date+timedelta(days=1)
        else:
            leave_count += 1
            total_days_count = total_days_count-1
        
    total_hours = (total_days_count*520)*60
        
    try:
        working_hours = (user.attendance_logs.filter(date__range=(month_start_date, month_last_date)).aggregate(sum=Sum('user_logs_summary__duration'))['sum']).total_seconds()
    except:
        working_hours = 0
    short_hours = total_hours - working_hours if (total_hours - working_hours) > 0 else 0
    
    ctx = {
        'user':user,
        'total_working_days':total_working_days,
        'total_present_days': UserAttendanceLog.objects.filter(user=user, date__range=(month_start_date, month_last_date)).exclude(user_logs_summary=None).count(),
        'leave':leave_count, 
        'short_hours': format_timedelta(timedelta(seconds=short_hours)),
        }

    return ctx