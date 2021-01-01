from django import template
from service.models import TimesheetFiled,ScheduleAllotment
from django.db.models import Sum
from attendance.models import Holidays
from datetime import date, datetime
import calendar
from django.db.models import Q
from attendance.models import UserAttendanceLogSummary
register = template.Library()


@register.simple_tag
def get_timesheet_value(date, type, user_id):
        if not type:
            timesheet_objects = TimesheetFiled.objects.filter(
                date=date, category__isnull=True, employee=user_id
            )
            timesheet_obj = timesheet_objects.aggregate(hours=Sum('hours'))

            timesheet_obj['title'] =  ";".join([tt.service.title + "-" + str(tt.hours)+"Hrs" for tt in timesheet_objects])

        else:
            timesheet_objects = TimesheetFiled.objects.filter(
                    date=date, category_id=type, employee=user_id
                )
            timesheet_obj = timesheet_objects.aggregate(hours=Sum('hours'))
            timesheet_obj['type'] = timesheet_objects.first() and timesheet_objects.first().category.title or ''
            timesheet_obj['title'] =  ";".join([tt.get_display_title or '' + "-" + str(tt.hours)+"Hrs" for tt in timesheet_objects])
        return timesheet_obj

@register.simple_tag
def get_total_timesheet_value(date, user_id):
    timesheet_obj = TimesheetFiled.objects.filter(
        date=date, employee=user_id,approve='approved'
    ).aggregate(total_hours=Sum('hours')).get('total_hours','')
    return timesheet_obj and timesheet_obj or ''

@register.simple_tag
def get_holidays_list(dates):
    holidays = Holidays.objects.filter(
        date__gte=dates[0], date__lte=dates[-1],type__in=['1','2']).values_list('date', flat=True)
    return list(holidays)

@register.simple_tag
def get_leave_list(dates):
    holidays = Holidays.objects.filter(
        date__gte=dates[0], date__lte=dates[-1],type__in=['1','2']).values_list('date', flat=True)
    return list(holidays)

@register.simple_tag
def empfreebusy_alloted_hours(user, date):
    alloted_hours = ScheduleAllotment.objects.filter(
        date=date, alloted_to = user)
    return sum([allot.hours for allot in alloted_hours])


@register.simple_tag
def timesheet_filled_by_other_listing(dates,user):
    filled_by_other = TimesheetFiled.objects.filter(date__gte=dates[0], date__lte=dates[-1],)
    filled_by_other = filled_by_other.filter(Q(help_to=user)|Q(meeting_with=user))
    return filled_by_other


@register.inclusion_tag('service/includes/approve_timehseet.html')
def approve_timehseet(user):
    timesheet_obj = TimesheetFiled.objects.filter(Q(help_to=user)|Q(meeting_with=user))
    timesheet_obj = timesheet_obj.filter(approve='new',category__field_type='user')
    return {'timesheet_obj':timesheet_obj,"heading":"Timesheet added for/with you,Take action!"}


@register.inclusion_tag('service/includes/approve_timehseet.html')
def tl_approve_timehseet(user):
    timesheet_obj = TimesheetFiled.objects.filter(category__isnull=False,approve='new',employee__parent=user)
    timesheet_obj = timesheet_obj.exclude(category__field_type='user')
    return {'timesheet_obj':timesheet_obj,"heading":"Timesheet added by your team members"}

@register.inclusion_tag('service/includes/approve_miss_punch.html')
def tl_approve_miss_punch(user):
    user_attendance_summary = UserAttendanceLogSummary.objects.filter(type='miss_punch', attendance_log__user__parent=user)
    return {'user_attendance_summary':user_attendance_summary,"heading":"Miss punch added by your team members"}

@register.inclusion_tag('service/includes/_reports_total_hours.html')
def get_month_hours(user, month=None, year=None):
    if not month and not year:
        month = date.today().month
        year = date.today().year
        total_days = date.today().day
    else:
        month = int(month)
        year = int(year)
        total_days = calendar.monthrange(year, month)[1]

    start_date = date(year=year, month=month, day = 1)
    end_date = date(year=year, month=month, day = total_days)
    total_hours = user.filled_by.filter(date__range=[start_date, end_date], category__isnull=True, service__type__in=['dedicated', 'hourly', 'estimation']).aggregate(total=Sum('hours'))
    total_hours = total_hours.get('total')
    incentive = 0

    if total_hours >= 120:
        incentive = 1000
    elif total_hours >= 150:
        incentive = ((incentive/100)*10) + incentive

    return {'total_hours':total_hours, 'user': user, 'incentive': incentive, 'remaining_hours': 120 - (total_hours or 0) }
