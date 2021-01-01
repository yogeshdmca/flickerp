from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import UserAttendanceLog, UserAttendanceLogSummary, Leave,LeaveCategory, WorkFromHome
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

def get_opportunity_data(request):
    attendance_id = request.GET.get('attendance_id')
    attendance_obj = UserAttendanceLog.objects.get(id = attendance_id)
    detailed_logs = attendance_obj.user_logs_summary.all().order_by('-pk')
    return render(request, 'attendance/partials/attendance-detail-list.html', {'detailed_logs':detailed_logs})

def get_leave(request):
    user_type = request.GET.get('user_type')
    leave_obj = Leave.objects.get(id = request.GET.get('leave_id'))
    user_leave_id = Leave.objects.filter(user_id = leave_obj.user_id, status__in=[2,3,4,5,6]).order_by('-date')[:5][::-1]
    return render(request, 'attendance/partials/leave_show.html', { 'user_leave_objs':user_leave_id, 'leave_obj':leave_obj, 'user_type':user_type })

def update_leave(request):
    leave_obj = Leave.objects.get(id = request.POST.get('leave_id'))
    status = request.POST.get('status',False)
    if status:
        leave_obj.status = status
        leave_obj.save()
    return JsonResponse({'success':1, 'action':'reload'})


def update_bulk_leaves(request):
    if request.is_ajax() and request.POST:
        leaves = Leave.objects.filter(id__in = request.POST.getlist('leaves[]'))
        if request.POST.get('action_type') == 'approve_all':
            leaves.update(management_approval='1')
        elif request.POST.get('action_type') == 'reject_all':
            leaves.update(management_approval='2')

        return JsonResponse({'success':1})

def request_for_leave_delete(request):
    try:
        leave = Leave.objects.get(pk=request.POST.get('leave_id',''))
        if leave.status == 1:
            leave.delete()
            return JsonResponse({'success':'1'})
    except:
        pass
    return JsonResponse({'success':'0'})

# def get_available_leave(request):
#     leave = LeaveCategory.objects.filter(user=request.user)
    
#     return JsonResponse({'success':'0'})


def request_for_wfh_delete(request):
    try:
        wfh = WorkFromHome.objects.get(pk=request.POST.get('wfh_id',''), status = '1')
        wfh.delete()
        return JsonResponse({'success':'1'})
    except:
        pass
    return JsonResponse({'success':'0'})


def add_comment_for_out_punch(request):
    if request.is_ajax() and request.POST:
        log_summary = UserAttendanceLogSummary.objects.get(pk=request.POST.get('pk'))
        log_summary.comment = request.POST.get('value')
        log_summary.type = 'miss_punch'
        log_summary.save()
        return JsonResponse({'success':'1'})

@csrf_exempt
def add_miss_punch(request, pk):
    if request.is_ajax() and request.POST:
        log = UserAttendanceLog.objects.get(pk=pk)
        in_time = datetime.strptime(request.POST.get('in_time'), '%H:%M').time()
        out_time = datetime.strptime(request.POST.get('out_time'), '%H:%M').time()
        if log.user_logs_summary.filter(type__in=['in', 'miss_punch'], in_time__range=(in_time, out_time)) or log.user_logs_summary.filter(out_time__range=(in_time, out_time)) or log.user_logs_summary.filter(type__in=['in', 'miss_punch'], in_time__lte=in_time, out_time__gte=out_time):
            return JsonResponse({'success':'1', 'msg':'Miss punch not added please check punch in Time.'})
        else:        
            summary = UserAttendanceLogSummary.objects.create(attendance_log_id=pk, duration=timedelta(hours=0), in_time=in_time, out_time=out_time, comment=request.POST.get('comment'), type='miss_punch')
            summary.duration = datetime.combine(datetime.min.date(), summary.out_time) - datetime.combine(datetime.min.date(), summary.in_time)
            summary.save()
            html_response = "<tr style='background-color:#ed5565; color:white;'><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"%(summary.in_time, summary.out_time, summary.duration, summary.comment)
            return JsonResponse({'success':'1', 'msg':'Miss punch added.', 'html_response':html_response})

@csrf_exempt
def approve_miss_punch(request):
    if request.is_ajax() and request.POST:
        log_summary = UserAttendanceLogSummary.objects.get(pk=request.POST.get('pk'))
        log_summary.type = 'in'
        log_summary.save()
        return JsonResponse({'success':'1'})

@csrf_exempt
def reject_miss_punch(request):
    if request.is_ajax() and request.POST:
        log_summary = UserAttendanceLogSummary.objects.get(pk=request.POST.get('pk'))
        log_summary.type = 'out'
        log_summary.save()
        return JsonResponse({'success':'1'})