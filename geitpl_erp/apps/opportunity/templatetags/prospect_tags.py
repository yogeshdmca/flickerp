from django import template
from service.models import Service
from django.db.models import Sum
from user.models import CustomUser
from dashboard.models import Notification
from datetime import date , timedelta, datetime
from opportunity.models import *
from opportunity.models import SCHEDULE_STATUS

def get_dict():
    return dict(SCHEDULE_STATUS)

register = template.Library()
@register.inclusion_tag('opportunity/partials/prospect_filter.html', takes_context=True)
def prospect_filters(context):
    tags = context['request'].user.get_sales_children_for_select_box()
    params  = context['request'].GET
    countries = Country.objects.all()
    
    SCHEDULE_STATUS = get_dict()
    for key in SCHEDULE_STATUS.keys():
        count = Opportunity.objects.filter(scheduler__result=key,user=context['request'].user).distinct().count()
        SCHEDULE_STATUS[key] = "%s (%s)"%(SCHEDULE_STATUS[key], count)

    return {'SCHEDULE_STATUS': SCHEDULE_STATUS,'tags':tags, 'current_user':context['request'].user,'params':params,'countries':countries}


@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()


# @register.inclusion_tag('users/partials/user_hierarchy_select.html', takes_context=True)
# def user_hierarchy_select_for_sales(context):
#     tags = context['request'].user.get_sales_children_for_select_box()
#     params  = context['request'].GET
#     return {'tags':tags, 'current_user':context['request'].user}


# @register.inclusion_tag('dashboard/partials/is_on_leave_notification.html')
# def leave_notifications():
#     leaves = Leave.objects.filter(date=date.today())
#     return {'leaves': leaves}


# @register.inclusion_tag('dashboard/partials/is_on_leave_notification.html')
# def supervisore_dashboard_notifications( user ):
#     leaves = Leave.objects.filter(date=date.today())
#     leave_list = Leave.objects.filter(user__in = self.request.user.childs.all())
#     return {'leaves': leaves}


# @register.filter
# def get_item_count(dictionary, key):
#     return dictionary.get(key)


# @register.simple_tag
# def get_date_range(date_from, date_to=None):
#     if not date_to:
#         date_to = date_from+timedelta(7)
#     date_list = []

#     while (date_from <= date_to):
#          date_list.append(date_from)
#          date_from = date_from+timedelta(days=1)
#     return date_list


# @register.filter
# def next_seven_days_schedule(user, service):
#     schedules = user.services_alloted.filter(date__gte = (datetime.now().date()), service = service)
#     return schedules if schedules.count() > 0 else None


# @register.inclusion_tag('dashboard/partials/schedule_timehseet.html')
# def schedule_timehseet_tag(user):
#     services = Service.objects.filter(allotments__alloted_to=user, allotments__date__week=date.today().isocalendar()[1]).distinct()
#     for service in services:
#         schedules = []
#         for i in range(0,6):
#             rdate =  date.today()-timedelta(date.today().weekday())+timedelta(i)
#             try:
#                 schedules.append(user.services_alloted.get(service = service ,date = rdate).hours)
#             except:
#                 schedules.append('')

#         service.schedules = schedules

#     date_list =[date.today()-timedelta(date.today().weekday())+timedelta(i) for i in range(0,6)]

#     return {'services': services, 'date_list':date_list}
