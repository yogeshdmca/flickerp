from django import template
from attendance.models import UserAttendanceLog, Holidays, Leave, WorkFromHome
from service.models import Service
from django.db.models import Sum
from user.models import CustomUser
from dashboard.models import Notification
from datetime import date , timedelta, datetime


register = template.Library()


@register.inclusion_tag('dashboard/partials/notifications.html', takes_context=True)
def recent_notifications(context):
    notifications = Notification.objects.filter(created_at__gte=date.today()-timedelta(days=6))[:5]
    return {'notifications': notifications}


@register.inclusion_tag('dashboard/partials/is_on_leave_notification.html')
def leave_notifications():
    leaves = Leave.objects.filter(date=date.today())
    return {'leaves': leaves}

@register.inclusion_tag('dashboard/partials/is_on_wfh_notification.html')
def wfh_notifications():
    wfh = WorkFromHome.objects.filter(date=date.today())
    return {'wfh': wfh}

@register.inclusion_tag('dashboard/partials/is_on_leave_notification.html')
def supervisore_dashboard_notifications( user ):
    leaves = Leave.objects.filter(date=date.today())
    leave_list = Leave.objects.filter(user__in = self.request.user.childs.all())
    return {'leaves': leaves}


@register.filter
def get_item_count(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def get_date_range(date_from, date_to=None):
    if not date_to:
        date_to = date_from+timedelta(7)
    date_list = []

    while (date_from <= date_to):
         date_list.append(date_from)
         date_from = date_from+timedelta(days=1)
    return date_list


@register.filter
def next_seven_days_schedule(user, service):
    schedules = user.services_alloted.filter(date__gte = (datetime.now().date()), service = service)
    return schedules if schedules.count() > 0 else None


@register.inclusion_tag('dashboard/partials/schedule_timehseet.html')
def schedule_timehseet_tag(user):
    services = Service.objects.filter(allotments__alloted_to=user, allotments__date__week=date.today().isocalendar()[1]).distinct()
    for service in services:
        schedules = []
        for i in range(0,6):
            rdate =  date.today()-timedelta(date.today().weekday())+timedelta(i)
            try:
                schedules.append(user.services_alloted.get(service = service ,date = rdate).hours)
            except:
                schedules.append('')

        service.schedules = schedules

    date_list =[date.today()-timedelta(date.today().weekday())+timedelta(i) for i in range(0,6)]

    return {'services': services, 'date_list':date_list}
