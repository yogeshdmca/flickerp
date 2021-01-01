from django.views import View
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from service.models import Service, ScheduleAllotment as ModelScheduleAllotment, TimesheetFiled, ServiceRecords
from service import SERVICE_STATUS
from datetime import datetime, timedelta, date
from service.forms import ScheduleAllotmentForm
from attendance.models import Holidays, this_month_start_end_date
from django.http import JsonResponse
from user.models import CustomUser
from dateutil import parser



class ServiceListing(View):
    template_name = 'service/supervisor/services.html'

    def get(self, request):
        services = {key: getattr(Service.objects, key)(user=request.user)
                    for key, value in SERVICE_STATUS
                    }
        print(services)
        return render(request,
                      self.template_name,
                      {
                          'services': services, 'SERVICE_STATUS': SERVICE_STATUS
                      }
                      )


class ServiceDetails(DetailView):
    model = Service
    template_name = "service/supervisor/service_detail.html"



class ManageProjectTlOtp(View):
    template_name = 'service/supervisor/service_otp.html'

    def get(self, request, pk,*args, **kwargs):
        #user = request.GET.get('tl_id', request.user.pk)

        services = Service.objects.get(pk=pk)
        tls = CustomUser.objects.filter(department__in=['2','5','6','7']).exclude(childs__isnull=True)

        return render(request, self.template_name,
                          {
                              'services': services,
                              'tls':tls
                          }
                      )
        
    def post(self, request,pk,*args, **kwargs):
        tl = request.POST.get('tl',False)
        start_date = parser.parse(request.POST.get('start_date',False))
        end_date = parser.parse(request.POST.get('end_date',False))
        hours = request.POST.get('hours',False)
        description = request.POST.get('description','')
        service = Service.objects.get(pk=pk)
        if tl and start_date and end_date and hours :
            service_record__add = ServiceRecords(start_date=start_date,end_date=end_date,title=description)
            service_record__del = ServiceRecords(start_date=start_date,end_date=end_date,title=description,action='2', service_id =pk )
            if service.type == "dedicated":
                service_record__add.total_hours = 0.0
                service_record__add.per_day = hours
                service_record__del.total_hours = 0.0
                service_record__del.per_day = hours
            else:
                service_record__add.total_hours = hours
                service_record__add.per_day = 0.0
                service_record__del.total_hours = hours
                service_record__del.per_day = 0.0
        else:
            return JsonResponse({'status':201,'data':'validation error '})


        if service.childs.filter(assigned_to=tl):
            service_record__add.service = service.childs.get(assigned_to=tl)
            service_record__add.save()
            service_record__del.save()
        else:
            service.pk = None
            service.assigned_to_id = tl
            service.parent_id = pk
            service.save()
            service_record__add.service = service
            service_record__add.save()
            service_record__del.save()
        return JsonResponse({'status':200,'data':'created'})
        

class ManageProjectDaily(View):
    template_name = 'service/supervisor/manage_project.html'

    def get(self, request):
        user = request.GET.get('tl_id', request.user.pk)

        services = Service.objects.open(assigned_to__id=user)
        return render(request, self.template_name,
                      {
                          'services': services
                      }
                      )


class ScheduleAllotment(View):
    template_name = 'service/includes/schedule_allotment.html'

    def get(self, request, *arg, **kwargs):
        service_id = kwargs.get('service_id', 0)
        service = Service.objects.get(pk=service_id)
        form = ScheduleAllotmentForm(user=request.user)
        return render(request, self.template_name, {'service': service, 'form': form, 'daterange': self.daterange()})

    def post(self, request, *arg, **kwargs):
        service_id = kwargs.get('service_id', 0)
        service = Service.objects.get(pk=service_id)
        start_date = datetime.strptime(request.POST.get('date'), "%m/%d/%Y")
        end_date = datetime.strptime(request.POST.get('date_to'), "%m/%d/%Y")
        #alloted_to = request.user.childs.get(id=request.POST.get('alloted_to'))
        alloted_to_id = request.POST.get('alloted_to')

        form = ScheduleAllotmentForm(user=request.user)
        holidays = [holiday['date'] for holiday in Holidays.objects.filter(
            date__range=(start_date, end_date),type__in=['1','2']).values('date')]
        total_days = int((end_date - start_date).days + 1)

        if request.POST.get('is_update') == 'True':
            ModelScheduleAllotment.objects.filter(service=service, date__range=(
                start_date, end_date), alloted_to_id=alloted_to_id).delete()
            if request.POST.get('is_delete') == 'True':
                return render(request, self.template_name, {'service': service, 'form': form, 'daterange': self.daterange()})

        if ((total_days - len(holidays)) * int(request.POST.get('hours')) > service.get_available_hours() and service.type != 'dedicated') or (service.type == 'dedicated' and service.get_available_hours() < int(request.POST.get('hours'))):
            return JsonResponse({'success': 0, 'msg': 'You are trying to allot more Hours then available hours. Available Hours - %s' % (service.get_available_hours())})

        for n in range(int((end_date - start_date).days + 1)):
            if not (start_date + timedelta(n)).date() in holidays:
                schedule, created = ModelScheduleAllotment.objects.get_or_create(
                    service=service, date=(start_date + timedelta(n)).date(), alloted_to_id=alloted_to_id)
                schedule.hours = request.POST.get('hours')
                schedule.save()

        return render(request, self.template_name, {'service': service, 'form': form, 'daterange': self.daterange()})

    def daterange(self):
        result = []
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=15)

        holidays = [holiday['date'] for holiday in Holidays.objects.filter(
            date__range=(start_date, end_date),type__in=['1','2']).values('date')]

        for n in range(int((end_date - start_date).days + 1)):
            if not (start_date + timedelta(n)).date() in holidays:
                result.append((start_date + timedelta(n)).date())

        return result[:7]




class EmpFreeBusy(View):

    template_name = 'service/supervisor/emp_free_busy.html'

    def get(self, request, *arg, **kwargs):
        from_date = kwargs.get('date', 0)
        tl = kwargs.get('tl', 0)
        start_date, end_date,tdays = this_month_start_end_date()
        
        if from_date:
            from_date = datetime.strptime(from_date, "%d-%m-%Y").date()

        else:
            from_date = date.today().day > 15 and start_date.replace(day=16) or start_date

        to_date = date.today().day > 15 and end_date or from_date.replace(day=15)



        if tl:
            user = CustomUser.objects.get(id=tl)
        else:
            user = request.user

        developers = user.get_all_childs_under_me()
        #tl = request.user.get_direct_supervisor_under_me

        #import pdb;pdb.set_trace()

        ctx = {
            'from_date':from_date,
            'to_date':to_date,
            'developers':developers,
            'dates':[from_date + timedelta(days=x) for x in range((to_date-from_date).days + 1)]
            #'tl':tl,

        }

        return render(request, self.template_name,ctx)
        

class UpdateService(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
            return super(UpdateService, self).dispatch(request, *args, **kwargs)

    def post(self,request):
        if request.is_ajax():
            service_id = request.POST.get('pk',False)
            try:
                ctx = {request.POST.get('name'): request.POST.get('value')}
                service = Service.objects.filter(pk = service_id)
                service.update(**ctx)
                data = {"msg":"Records updated",'status':'saved'}
            except:
                data = {"msg":"Invalid records",'status':'error'}
            return JsonResponse(data)

class Reports(View):
    template_name = 'service/supervisor/reports.html'

    def get(self, request):
        user_id = request.GET.get('supervisor')
        supervisor = None
        if user_id:
            supervisor = CustomUser.objects.get(id=user_id)
            users = supervisor.get_all_childs_under_me()
        else:
            users = request.user.get_all_childs_under_me()

        month = request.GET.get('month')
        year = request.GET.get('year')
        if month and year:
            month = int(month)
            year = int(year)
        else:
            month = date.today().month
            year = date.today().year

        supervisors = request.user.get_all_supervisors_under_me(include_self=False)
        month_dict = [{'id':i, 'month_name': date(date.today().year, i, 1).strftime('%B')} for i in range(1, 13)]
        year_dict = [{'id':i, 'year': i} for i in range(2017, int(date.today().year) + 2)]
        return render(request, self.template_name, {'users':users, 'month':month , 'year':year, 'month_dict': month_dict, 'year_dict': year_dict, 'supervisors': supervisors, 'supervisor':supervisor})
        