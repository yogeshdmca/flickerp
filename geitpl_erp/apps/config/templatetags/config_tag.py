from django import template
from service.models import TimesheetFiled,ScheduleAllotment
from django.db.models import Sum
from attendance.models import Holidays
from datetime import date, datetime
import calendar
from django.conf import settings

register = template.Library()




@register.simple_tag
def site_name():
    return settings.WEBSITE_NAME

@register.simple_tag
def site_sort_name():
    return settings.WEBSITE_SORT_NAME

@register.simple_tag
def site_admin_email():
    return settings.ADMIN_EMAIL


# @register.simple_tag
# def get_leave_list(dates):
#     holidays = Holidays.objects.filter(
#         date__gte=dates[0], date__lte=dates[-1],type__in=['1','2']).values_list('date', flat=True)
#     return list(holidays)

