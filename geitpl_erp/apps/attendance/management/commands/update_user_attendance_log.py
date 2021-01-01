from django.core.management.base import BaseCommand
from attendance.models import AttendanceMachineLog, UserAttendanceLog, UserAttendanceLogSummary
from user.models import CustomUser
from datetime import datetime, date, timedelta

class Command(BaseCommand):
    help = 'Update User Attendance Logs'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=int)
        parser.add_argument('--start_date', type=str)
        parser.add_argument('--end_date', type=str)

    def handle(self, *args, **options):
        flag = False
        user_id = options['user']
        start_date = options['start_date']
        end_date = options['end_date']

        if user_id:
            users = CustomUser.objects.filter(id=user_id)
        else:
            users = CustomUser.objects.filter(is_superuser=False)

        if not start_date:
            start_date = date.today().replace(day=1)
        else:
            start_date = datetime.strptime(start_date ,'%Y-%m-%d')

        if not end_date:
            end_date = date.today()
        else:
            end_date = datetime.strptime(end_date ,'%Y-%m-%d')

        while(True):
            if start_date == end_date:
                break

            for user in users:
                try:
                    shift = user.shifts.get(date=start_date.date())
                    

                    if shift.shift.shift_type != 0:
                        s_date = datetime.combine(start_date.date(), shift.shift.time_from) - timedelta(hours=3)
                        e_date = datetime.combine(start_date.date(), shift.shift.time_from) + timedelta(hours=shift.shift.shift_type + 5)
                        time_logs = AttendanceMachineLog.objects.filter(mu_id=user.machine_id, datetime__range=(s_date, e_date) ).values_list('datetime')
                        u_a_log, created = UserAttendanceLog.objects.get_or_create(user=user, date=start_date, shift=shift)

                        if len(time_logs) == 1:
                            time_obj = time_logs[0][0]
                            #check if single punch in day found according to shift
                            if time_obj.hour < shift.shift.time_from.hour + (shift.shift.shift_type/2):
                                in_time = time_obj
                                out_time = (time_obj + timedelta(hours=1)).time()
                            else:
                                out_time = time_obj
                                in_time = (time_obj - timedelta(hours=9)).time()

                            duration = timedelta(hours=8)
                            UserAttendanceLogSummary.objects.get_or_create(attendance_log = u_a_log, in_time = in_time, out_time = out_time, type = 'miss_punch', duration = duration)
                        else:
                            for log_index in range(len(time_logs)-1):
                                if (log_index + 1) % 2 == 0:
                                    type = 'out'
                                else:
                                    type = 'in'
                                in_time = time_logs[log_index][0]

                                out_time = (time_logs[log_index + 1][0]-timedelta(minutes=1))
                                in_time_only = (time_logs[log_index][0]).time()
                                out_time_only = (time_logs[log_index + 1][0]-timedelta(minutes=1)).time()
                                duration = out_time - in_time
                                if duration < timedelta(minutes=3):
                                    out_time = time_logs[log_index + 1][0]
                                    duration = out_time - in_time
                                    out_time_only = (time_logs[log_index + 1][0]-timedelta(minutes=0)).time()

                                #in_time_only = (time_logs[log_index][0]).time()).time()

                                #out_time_only = (time_logs[log_index + 1][0]-timedelta(minutes=1)).time()

                                
                                UserAttendanceLogSummary.objects.get_or_create(attendance_log = u_a_log, in_time = in_time_only, out_time = out_time_only, type = type, duration = duration)
                except Exception as e:
                    print('>>>>>>>>>>>>>>>>>>>>', e, user)
                

            start_date = start_date + timedelta(days=1)

        if flag:
            exit(0)
