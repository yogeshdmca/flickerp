from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, DeleteView, CreateView, DetailView
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.db.models import Sum
from .models import AttendanceMachineLog, UserAttendanceLog, Holidays, Leave, LeaveCategory, WorkFromHome, UserAttendanceLogSummary,EmployeeShift, Shift
from user.models import CustomUser
from .forms import HolidayCreateForm, LeaveCreateForm, AdministrationLeaveCreateForm, WFHCreateForm
from django.core.urlresolvers import reverse, reverse_lazy
from datetime import date, timedelta, datetime
from calendar import monthrange
from django.conf import settings
from io import TextIOWrapper
from django.core.management import call_command
from config import week_range, date_range, SHIFT_SELECT

class AdministrationAttendanceListView(TemplateView):
    template_name = 'attendance/attendance_list.html'

    @staticmethod
    def get_filter_data():
        month_dict = [{'id':i, 'month_name': date(date.today().year, i, 1).strftime('%B')} for i in range(1, 13)]
        year_dict = [{'id':i, 'year': i} for i in range(2017, int(date.today().year) + 2)]
        return {
            'month_dict':month_dict,
            'year_dict':year_dict
        }


    def get_context_data(self, **kwargs):
        context = super(AdministrationAttendanceListView, self).get_context_data(**kwargs)
        context.update(dict(self.request.GET))
        context.update(dict(self.get_filter_data()))
        if self.request.GET.get('user'):
            user_id=self.request.GET.get('user')
            user_id = CustomUser.objects.get(pk=user_id)
            if user_id not in self.request.user.get_all_childs_under_me():
                user_id=self.request.user
        else:
            user_id=self.request.user

        context['user'] = user_id
        context['user_id'] = self.request.GET.get('user', self.request.user.id)
        context['select_user'] = user_id and user_id or self.request.user

        context['total_hours_in_month'] = self.total_hours_in_month(user_id)
        context['attendance_logs'] = self.get_attendence_line(user=user_id)
        context['total_working_hours'] = self.total_working_hours(context['attendance_logs'])
        return context

    def get_year_month(self):
        if self.request.GET.get('month') and self.request.GET.get('year'):
            month = int(self.request.GET.get('month'))
            year = int(self.request.GET.get('year'))
        else:
            last_record = UserAttendanceLog.objects.last().date
            month = last_record.month
            year = last_record.year
        return (month, year)

    def get_attendence_line(self,user):
        month, year  = self.get_year_month()
        return UserAttendanceLog.objects.filter(date__month=month, date__year=year,user=user)

    def total_hours_in_month(self,user):
        month, year  = self.get_year_month()
        last_record = UserAttendanceLog.objects.last().date
        hours = EmployeeShift.objects.filter(date__lte=last_record, date__month=month, date__year=year,user=user).exclude(shift__shift_type=0).aggregate(hours = Sum('shift__shift_type')).get('hours')
        return hours and "%s hours and Hrs"%(hours) or "0 Hrs"

    def total_working_hours(self,records):
        duration = records.filter(user_logs_summary__type='in').aggregate(durations=Sum('user_logs_summary__duration'))['durations']
        return duration and self.second_to_duration(duration.total_seconds()) or "0 Hrs"

    def second_to_duration(self,seconds):
        min, sec = divmod(seconds, 60) 
        hour, min = divmod(min, 60) 
        return "%s Hrs, %2s Minute" % (hour, min) 


class CommonAttendanceListView(AdministrationAttendanceListView):
    template_name = 'attendance/common_attendance_list.html'


def attendance_upload(request):
    users = CustomUser.objects.all()
    if request.GET:
        return render(request, 'attendance/attendance_upload.html', {"users":users})
    
    elif request.POST:
        f = TextIOWrapper(request.FILES['attendance_file'].file, encoding='utf-8')
        datContent = [i.strip().split() for i in f.readlines()]
        AttendanceMachineLog.objects.all().delete()
        for data in datContent:
            AttendanceMachineLog.objects.create(mu_id=data[0], date=data[1], time=data[2], datetime=data[1]+ ' ' +data[2])
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        user = request.POST['user']
        call_command('update_user_attendance_log', user = user, start_date = start_date, end_date = end_date)
    return render(request, 'attendance/attendance_upload.html', {"users":users})

class AdministrationHolidayCreateView(CreateView):
    form_class = HolidayCreateForm
    template_name = 'attendance/holiday_list.html'
    success_url = reverse_lazy('attendance:holiday-list')

    def form_valid(self, form):
        response = super(AdministrationHolidayCreateView, self).form_valid(form)
        return response   

    def get_context_data(self, **kwargs):
        context = super(AdministrationHolidayCreateView, self).get_context_data(**kwargs)
        context['object_list'] = Holidays.objects.filter(type__in=['1','3'], date__year=date.today().year).order_by('date')
        return context

class AdministrationLeaveCreateView(CreateView):
    form_class = AdministrationLeaveCreateForm
    template_name = 'attendance/leave_listing.html'
    success_url = reverse_lazy('attendance:leave')

    def form_valid(self, form):
        response = super(AdministrationLeaveCreateView, self).form_valid(form)
        return response   

    def get_context_data(self, **kwargs):
        context = super(AdministrationLeaveCreateView, self).get_context_data(**kwargs)
        context['object_list'] = Leave.objects.filter( user = self.request.user ).order_by('-date')
        context['users'] = CustomUser.objects.all()
        return context

# class AdministrationApproveLeaveListView(ListView):
#     template_name = 'attendance/approve_leave_admin.html'
#     queryset = Leave.objects.all().order_by('-supervisor_approval','date')

#     def get_context_data(self, **kwargs):
#         context = super(AdministrationApproveLeaveListView, self).get_context_data(**kwargs)
        
#         if self.request.GET != {}:
#             month = self.request.GET.get('month', date.today().month)
#             year = self.request.GET.get('year', date.today().year)
#             last_day = monthrange(int(year), int(month))[1]
#             start_date = date.today().replace(day=1, month=int(month), year=int(year))
#             last_date = date.today().replace(day=last_day, month=int(month), year=int(year))
#             leaves_management = self.queryset.filter(date__range=(start_date, last_date))
#             leaves_supervisor = self.queryset.filter(user__in = self.request.user.childs.all(), date__range=(start_date, last_date))
#             user__in = self.request.user.childs.all()
#         else:
#             month = int(date.today().month)
#             start_month = date(date.today().year, month, 1)
#             leaves_management = self.queryset.filter(date__gte =(start_month))
#             leaves_supervisor = self.queryset.filter(user__in = self.request.user.childs.all(), date__gte =(start_month))
#         context['month'] = month

#         if self.request.GET.get('year'):
#             year = int(self.request.GET.get('year'))
#         else:
#             year = int(date.today().year)
#         context['year'] = year

#         context['leaves_management'] = leaves_management
#         context['leaves_supervisor'] = leaves_supervisor
#         context['year_dict'] = [{'id':i, 'year': i} for i in range(2017, int(date.today().year) + 2)]
#         context['month_dict'] = [{'id':i, 'month_name': date(date.today().year, i, 1).strftime('%B')} for i in range(1, 13)]
#         return context

# class AdministrationLeaveBank(CreateView):
#     form_class = LeaveBankForm
#     template_name = 'attendance/leave_bank_create.html'
#     success_url = reverse_lazy('attendance:administration-leave-bank')

#     def get_context_data(self, **kwargs):
#         context = super(AdministrationLeaveBank, self).get_context_data(**kwargs)
#         context['object_list'] = LeaveBank.objects.all().order_by('-created_at')[:30]
#         context['users'] = CustomUser.objects.all()
#         return context


class AdministrationMonthlyAttendanceListView(ListView):
    model = CustomUser
    template_name = 'attendance/monthly_attendance_list.html'
    queryset = CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AdministrationMonthlyAttendanceListView, self).get_context_data(**kwargs)
        holiday_count = 0
        month = int(self.request.GET.get('month')) if self.request.GET.get('month') else date.today().month - 1
        month_days = monthrange(date.today().year, month)[1]
        start_date = date(2017, month, 1)
        last_date = date(2017, month, month_days)
        holidays = Holidays.objects.filter(date__range=(start_date, last_date))

        for holiday in holidays:
            if holiday.end_date:
                holiday_count += (holiday.end_date - holiday.date).days + 1
            else:
                holiday_count += 1

        context['total_working_days'] = month_days - holiday_count
        context['month'] = month
        context['holidays'] = holidays
        context['month_dict'] = [{'id':i, 'month_name': date(2017, i, 1).strftime('%B')} for i in range(1, 13)]
        return context


class CommonHolidayList(ListView):
    template_name = 'attendance/holiday_list.html'
    queryset = Holidays.objects.filter(type__in=['1','3'], date__year=date.today().year).order_by('date')


class CommonLeaveListView(ListView):
    template_name = 'attendance/leave_listing.html'
    model = Leave

    def get_queryset(self, *args, **kwargs):
     return self.model.objects.filter(user=self.request.user).order_by('-date')


class CommonWFHListView(ListView):
    template_name = 'attendance/work_from_home_list.html'
    model = WorkFromHome

    def get_queryset(self, *args, **kwargs):
     return self.model.objects.all().filter(user=self.request.user).order_by('-date')


class CommonWFHCreateView(CreateView):
    form_class = WFHCreateForm
    template_name = 'attendance/partials/wfh_request_form.html'

    def post(self, request):
        form = WFHCreateForm(request.POST)
        if form.is_valid():
            wfh = form.save(commit = False)
            #import pdb;pdb.set_trace()
            wfh.user = request.user
            wfh.supervisor = request.user.parent
            try:
                wfh.save()
                msg = "Work from Home for Date %s created , Please ask from %s for approve"%(wfh.date, wfh.supervisor.get_full_name)
                success = '1'
            except Exception as e:
                msg=str(e)
                success="0"
        else:
            msg = "Form Is not valid, Please Check the details!!"
            success = '0'
        return JsonResponse({'success':success,'msg':msg}) 

class CommonLeaveCreateView(CreateView):
    form_class = LeaveCreateForm()
    template_name = 'attendance/partials/leave_request_form.html'

    def get(self, request):
        self.form_class.fields["category"].queryset =  LeaveCategory.objects.filter(user=request.user)
        ctx = {'form':self.form_class}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = LeaveCreateForm(request.POST)
        if form.is_valid():
            leave = form.save(commit = False)
            leave.user = request.user
            leave.manager = request.user.parent
            leave.shift = request.user.shifts.get(date=leave.date)
            leave.save()
            return JsonResponse({'success':"1",'msg':"Leave Created"}) 
        else:
            print(form.errors)
            return JsonResponse({'success':"0",'msg':"Leave Is not valid!"})


    def get_context_data(self, **kwargs):
        context = super(CommonLeaveCreateView, self).get_context_data(**kwargs)
        context['object_list'] = Leave.objects.filter(user=self.request.user).order_by('-date')
        context['optional_leaves']  = Holidays.objects.filter(type='3', date__gte=date.today())
        return context

class CommonApproveLeaveListView(ListView):
    model = Leave
    template_name = 'attendance/approve_leave.html'

    def get_queryset(self, *args, **kwargs):

     return Leave.objects.filter(user__in = self.request.user.childs.all(),status__in=[1,2,3,4,5,6])

    # def get_context_data(self, **kwargs):
    #     context = super(CommonApproveLeaveListView, self).get_context_data(**kwargs)
    #     if self.request.GET != {}:
    #         month = self.request.GET.get('month', date.today().month)
    #         year = self.request.GET.get('year', date.today().year)
    #         last_day = monthrange(int(year), int(month))[1]
    #         start_date = date.today().replace(day=1, month=int(month), year=int(year))
    #         last_date = date.today().replace(day=last_day, month=int(month), year=int(year))
    #         objects_month = self.queryset.filter(user__in = self.request.user.childs.all(), date__range=(start_date, last_date))
    #     else:
    #         month = int(date.today().month)
    #         start_month = date(date.today().year, month, 1)
    #         objects_month = self.queryset.filter(user__in = self.request.user.childs.all(), date__gte =(start_month))
    #     context['month'] = month

    #     if self.request.GET.get('year'):
    #         year = int(self.request.GET.get('year'))
    #     else:
    #         year = int(date.today().year)
    #     context['year'] = year

    #     context['month_dict'] = [{'id':i, 'month_name': date(date.today().year, i, 1).strftime('%B')} for i in range(1, 13)]
    #     context['year_dict'] = [{'id':i, 'year': i} for i in range(2017, int(date.today().year) + 2)]
    #     context['object_list'] = objects_month
    #     return context

# class HRLeaveCreateView(CreateView):
#     form_class = LeaveCreateForm
#     template_name = 'attendance/leave_listing.html'
#     success_url = reverse_lazy('attendance:leave')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         response = super(HRLeaveCreateView, self).form_valid(form)
#         return response

#     def get_context_data(self, **kwargs):
#         context = super(HRLeaveCreateView, self).get_context_data(**kwargs)
#         context['object_list'] = Leave.objects.filter(user=self.request.user).order_by('-date')
#         return context

# class HRApproveLeaveListView(ListView):
#     model = Leave
#     template_name = 'attendance/approve_leave.html'

#     def get_context_data(self, **kwargs):
#         context = super(CommonApproveLeaveListView, self).get_context_data(**kwargs)
#         context['object_list'] = Leave.objects.filter(user__in = self.request.user.childs.all()).order_by('-date')
#         return context


# def approve_leave_every_month():
#     month = datetime.now().month
#     leave_obj = Leave.objects.filter(date__month__lt = month)
#     for leave in leave_obj:
#         if leave.supervisor_approval == '0':
#             leave.supervisor_approval = '1'
#             leave.management_approval = '1'
#         elif leave.management_approval == '0':
#             leave.management_approval = '1'
#         else:
#             print ('.....')
#         leave.save()


class ShiftListCreate(View):
    model = EmployeeShift
    template_name = "attendance/shift_list_create.html"
    #form_class = EmployeeShiftForm
    def get(self, request, *args, **kwargs):
        #object_list = self.model.objects.filter(date__range=week_range(date.today()))

        dates = date_range(date.today(), date.today()+timedelta(days=10))

        users = CustomUser.objects.filter( parent__isnull=False)

        return render(request, self.template_name, {'users':users,'dates':dates,'shifts':Shift.objects.filter(is_active=True,shift_type__in=[9,10])})

    def post(self, request, *args, **kwargs):
        user = request.POST.get('user')
        shift_id = request.POST.get('shift_id')

        start_date = request.POST.get('start_date',False)
        end_date = request.POST.get('end_date',False)

        if start_date and end_date :
            start_date = datetime.strptime(start_date, '%m/%d/%Y')
            end_date = datetime.strptime(end_date, '%m/%d/%Y')
        else :
            return HttpResponseRedirect(reverse('attendance:humanresource-shift-list-create'))

        if user == 'all':
            users = CustomUser.objects.filter(parent__isnull=False)
        else:
            users = CustomUser.objects.filter(id=user)

        while start_date <= end_date:
            for user in users:
                holidays = Holidays.objects.filter(date=start_date, type__in=['1', '2'])
                if holidays:
                    shift = Shift.weekoff_shift()
                else:
                    shift = Shift.objects.get(id=shift_id)

                shift_obj, created = self.model.objects.update_or_create(user=user,date = start_date,defaults={'updated_by':request.user, 'shift':shift})
            start_date = start_date+timedelta(days=1)

        return HttpResponseRedirect(reverse('attendance:humanresource-shift-list-create'))
