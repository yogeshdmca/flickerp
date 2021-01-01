# Create new User
from django.views.generic import View, ListView
from user.models import *
from user.forms import UserLoginForm, SkillCreateForm, FamilyMemberForm,UserCreateForm
from django.http import JsonResponse
from datetime import datetime , timedelta
from dateutil import parser
from attendance.models import Holidays

class UserListView(ListView):
    model = CustomUser
    queryset = CustomUser.objects.filter(parent__isnull=False)
    paginate_by = 50
    template_name = 'users/administration/user_listing.html'


def event_calnder(request):

    start_date = parser.parse(request.GET.get('start'))
    end_date = parser.parse(request.GET.get('end'))
    data = []
    for shift in request.user.shifts.filter(date__range=(datetime.now(), datetime.now()+timedelta(days=30))).order_by('date') :
        if shift.shift.shift_type  is 0:
            ctx = {'title':shift.shift.display_shift,'start':str(shift.date)}
        else:
            ctx = {'title':shift.shift.display_shift, 'start':str(shift.date)}
        data.append(ctx)

    for service in request.user.services_alloted.filter(date__range=(start_date,end_date)).order_by('date'):
        ctx = {'title':service.description,'start':service.date}
        data.append(ctx)

    for holiday in Holidays.objects.filter(type__in=['1'],date__range=(start_date,end_date)):
        ctx = {'title':holiday.description,'start':holiday.date}
        data.append(ctx)

    for wfh in request.user.wfh.filter(date__range=(start_date,end_date)):
        ctx = {'title':"Work from home",'start':wfh.date}
        data.append(ctx)

    # for log in request.user.attendance_logs.filter(date__lte=end_date, date__gte=start_date)
    #     half_days = [log for log in attendance_logs if not log.is_fullday]

    #NEED TO CHECK SORT HOURS 


    return JsonResponse(data,safe=False)
