from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from datetime import date, datetime, timedelta
from service.models import TimesheetFiled
from service.utils import get_month_date
from service.models import TimesheetType, TimesheetFiled, ScheduleAllotment
from service.models import TIMESHEET_TYPE, Service
from user.models import CustomUser
from opportunity.models import Client


class TimesheetView(View):
    template_name = 'service/employee/timesheet.html'

    def get(self, request):
        dates = list(get_month_date())
        types = TimesheetType.objects.all()

        tl_hierarchy = request.user.get_all_childs_under_me()

        user_id = request.GET.get('user', request.user.id)
        try:
            user = CustomUser.objects.get(id=request.GET.get('user'))
        except:
            user = request.user

        return render(request, self.template_name,
                      {
                          'dates': dates,
                          'types': types,
                          'user_id': user_id,
                          'user_timesheet':user,
                          'tl_hierarchy': tl_hierarchy
                      }
                      )


class FillTimesheetView(View):
    template_name = 'service/includes/fill_timesheet.html'

    def get_timesheet_date(self):
        timesheet_date = date.today()
        shift = self.request.user.shifts.get(date=date.today())
        if shift.shift.shift_type == 0:
            shift = self.request.user.shifts.get(date=date.today() - timedelta(days=1))
            if shift.get_extended_time_to() > datetime.now():
                timesheet_date = shift.date


        elif shift.get_extended_time_from() < datetime.now():
            timesheet_date = date.today()
        else:
            timesheet_date = date.today() - timedelta(days=1)

        return timesheet_date


    def get(self, request):
        timesheet_date = self.get_timesheet_date()

        timesheet_todays = TimesheetFiled.objects.filter(
            employee=request.user, date=timesheet_date, category__isnull=True)

        service_list = [timesheet.service for timesheet in timesheet_todays]

        service_assined = ScheduleAllotment.objects.filter(
            date=timesheet_date, alloted_to=request.user).exclude(
            service__in=service_list
            )

        task_todays = TimesheetFiled.objects.filter(
            employee=request.user, date=timesheet_date, category__isnull=False)

        return render(request, self.template_name,
                      {
                          'service_assined': service_assined,
                          'TIMESHEET_TYPE': TIMESHEET_TYPE,
                          'timesheet_todays': timesheet_todays,
                          'task_todays': task_todays
                      }
                      )

    def post(self, request):
        timesheet_date = self.get_timesheet_date()
        service_alloted_ids = request.POST.getlist('service_id', [])
        added_value_on_alloted = request.POST.getlist('service_value', [])

        timesheet_type = request.POST.getlist('timesheet_type', [])
        timesheet_category = request.POST.getlist('timesheet_category', [])
        suportives = request.POST.getlist('suportive', [])
        hours = request.POST.getlist('task_value', [])
        field_types = request.POST.getlist('field_type', [])

        for index, alloted_id in enumerate(service_alloted_ids):
            schedule_allotment = ScheduleAllotment.objects.get(id=alloted_id)
            if added_value_on_alloted[index]:
                fill_hours_on_service = float(added_value_on_alloted[index])
            else:
                continue

            if fill_hours_on_service > schedule_allotment.hours:
                fill_hours_on_service = schedule_allotment.hours

            ctx = {'hours': fill_hours_on_service}

            TimesheetFiled.objects.update_or_create(
                employee=request.user, category=None, service=schedule_allotment.service, date=timesheet_date, defaults=ctx)

        #  end of code for filling assined task and service
        # start filling  task of daily work

        if len(timesheet_type) == len(hours):

            for index, task_category in enumerate(timesheet_type):
                task_sub_category = timesheet_category[index]

                suportive = suportives[index]

                hour = hours[index]
                field_type = field_types[index]

                ctx = {'hours': hour}

                timesheet_ctx = {
                    'employee':request.user, 
                    'category_id':task_sub_category, 
                    'date':timesheet_date,
                    'approve':'new',
                    }

                if field_type in ['service', 'client']:
                    timesheet_ctx.update({'service_id': suportive})

                if field_type == 'text':
                    timesheet_ctx.update({'description': suportive})

                if field_type == 'user':
                    timesheet_ctx.update({'help_to_id': suportive})

                TimesheetFiled.objects.update_or_create(defaults=ctx,**timesheet_ctx)
        else:
            return JsonResponse({'error': "task records not added correct , please check and add again", 'added': 'false'})

        return JsonResponse({'added': 'true'})


def get_timesheet_category_type(request):
    timesheet_type = request.GET.get('timesheet_type', False)

    types = TimesheetType.objects.filter(type=timesheet_type)

    print (types, timesheet_type)

    return render(request, 'service/includes/get_timesheet_category_type.html', {'types': types})


def add_new_timesheet_record(request):

    return render(request, 'service/includes/_timesheet_task_create.html', {'TIMESHEET_TYPE': TIMESHEET_TYPE, })


def get_timesheet_sub_category_type(request):

    timesheet_category = request.GET.get('timesheet_category', False)

    category = TimesheetType.objects.get(id=timesheet_category)

    users = CustomUser.objects.filter(parent__isnull=False)

    services = Service.objects.open(
        assigned_to__in=[request.user, request.user.parent])

    clients = Client.objects.all()

    ctx = {
        'category': category,
        'users': users,
        'services': services,
        'clients': clients,
    }

    return render(request, 'service/includes/get_timesheet_sub_category_type.html', ctx)


def get_timesheet_type_line(request):
    select_type = request.GET.get('type_id', False)

    type = TimesheetType.objects.filter(type=select_type)

    # if select_type in ["meeting"]:
    #     suportive = CustomUser.objects.filter(parent__isnull=False)
    # elif select_type in ["service"]:
    #     suportive = Service.objects.open(
    #         assigned_to__in=[request.user, request.user.parent])
    # else:
    #     suportive = False

    ctx = {'type': type, 'select_type': select_type, 'select_type_value': dict(
        TIMESHEET_TYPE).get(select_type), 'suportive': suportive}

    return render(request, 'service/includes/get_timesheet_type_line.html', ctx)


def delete_timesheet_task_record(request):
    select_type = request.GET.get('timesheet_id', False)
    try:
        TimesheetFiled.objects.get(pk=select_type).delete()
        return JsonResponse({'deleted': 'true'})
    except:
        return JsonResponse({'deleted': 'false'})



class RejectTimesheet(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
            return super(RejectTimesheet, self).dispatch(request, *args, **kwargs)

    def post(self,request):
        if request.is_ajax():
            time_sheet_id = request.POST.get('pk',False)            
            #try:
            time_sheet_obj = TimesheetFiled.objects.get(pk=time_sheet_id)
            time_sheet_obj.approve = 'rejected'
            time_sheet_obj.approver_user = request.user
            time_sheet_obj.save()
            data = {"msg":"Records deleted",'success':'true'}
            return JsonResponse(data)


class ApproveTimesheet(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
            return super(ApproveTimesheet, self).dispatch(request, *args, **kwargs)

    def post(self,request):
        if request.is_ajax():
            time_sheet_id = request.POST.get('pk',False)            
            #try:
            time_sheet_obj = TimesheetFiled.objects.get(pk=time_sheet_id)
            time_sheet_obj.approve = 'approved'
            time_sheet_obj.approver_user = request.user
            time_sheet_obj.save()
            data = {"msg":"Records approved",'success':'true'}
            return JsonResponse(data)
