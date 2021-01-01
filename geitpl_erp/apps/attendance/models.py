from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models.functions import Coalesce

from user.models import CustomUser
from django.db.models import F, Count, Value, Sum, Q
from django.conf import settings
from config import TIME_SELECT , SHIFT_SELECT, LCY, LRT,LRS #LEAVE_FOR, LEAVE_TYPE 
from config.models import Year
from datetime import datetime, date, timedelta, time
import time
import calendar


def month_start_end_date(month, year):
    days = calendar.monthrange(year, month)[-1]
    start_date = date(year,month,1)
    end_date = date(year,month,days)
    return start_date, end_date, days
    


def this_month_start_end_date():
    start_date = date.today().replace(day=1)
    tmp_date = start_date+timedelta(days=35)
    tmp_date = tmp_date.replace(day=1)
    end_date = tmp_date-timedelta(days=1)
    total_days = (end_date-start_date).days+1
    return start_date,end_date,total_days


def last_month_start_end_date():
    tmp_date = date.today().replace(day=1)
    end_date = tmp_date-timedelta(days=1)
    start_date = end_date.replace(day=1)
    total_days = (end_date-start_date).days+1
    return start_date,end_date,total_days


class Shift(models.Model):
    time_from = models.TimeField("Start time",null=True, blank=True)
    time_to = models.TimeField("End time",null=True, blank=True)
    shift_type = models.IntegerField(choices=[(9,'9 Hours'),(10, '10 Hours'),(0,'Weekly off')], default=9)
    weekday = models.IntegerField(choices=[(5,'5 Days'),(6, '6 Days')], null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.shift_type is 0:
            return self.get_shift_type_display()
        return "%s - %s/%s"%(self.time_from.strftime('%I %p'), self.time_to.strftime('%I %p'), self.get_shift_type_display())

    @property
    def display_shift(self):
        if self.shift_type is 0:
            return self.get_shift_type_display()
        return "%s - %s"%(self.time_from.strftime('%I %p'), self.time_to.strftime('%I %p'))

    @classmethod
    def weekoff_shift(cls):
        return cls.objects.get(shift_type=0)


class EmployeeShift(models.Model):
    user = models.ForeignKey(CustomUser, related_name='shifts',limit_choices_to={'is_active': True})
    date = models.DateField()
    shift = models.ForeignKey(Shift, null=True, related_name='shifts')
    updated_by = models.ForeignKey(CustomUser, related_name='shifts_updated_by')
    #weekoff = models.CharField("Weekly Off Day",max_length=100,null=True, blank=True)

    def get_extended_time_from(self):
        return datetime.combine(self.date, self.shift.time_from) - timedelta(hours=2)

    def get_extended_time_to(self):
        return self.get_extended_time_from() + timedelta(hours=self.shift.shift_type + 4)

    @property
    def get_start_datetime(self):
        return datetime.combine(self.date,self.shift.time_from)

    @property
    def get_end_datetime(self):
        return datetime.combine(self.date,self.shift.time_to)

    def __str__(self):
        return "%s %s"%(self.user, self.date)


class AttendanceMachineLog(models.Model):
    mu_id = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    datetime = models.DateTimeField(null=True)


class UserAttendanceLog(models.Model):
    user = models.ForeignKey(CustomUser, related_name='attendance_logs')
    date = models.DateField()
    shift = models.OneToOneField(EmployeeShift, related_name='attandance_log', null=True)


    @property
    def get_daily_salary(self):
        start_date, end_date, days = month_start_end_date(self.date.month, self.date.year)
        #pdays = type(self).get_preset_days(self.user,start_date,end_date)
        shifts = self.user.shifts.filter(date__range=(start_date, end_date)).exclude(shift__shift_type=0).count()
        contract = self.user.contracts.filter(is_active = True).first()

        if contract:
            daily_salary = contract.total_salary()/shifts
        else:
            daily_salary = 0.0
        return  round(daily_salary, 2)

    def sum_of_time(self, timeList):
        from datetime import time
        totalSecs = 0
        for tm in timeList:
            timeParts = [int(s) for s in tm.split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        #return "%s:%s:%s"%(hr, min, sec)
        return time(hr, min, sec)


    @property
    def leave(self):
        try:
            partial_leave = Leave.objects.get(leave_for__in=['6.5','5','2.5','1'], date=self.date, user=self.user)
            return partial_leave
        except:
            return self.is_full_day_leave

    @property
    def is_full_day_leave(self):
        try:
            leave = self.user.leaves.get(date__lte=self.date, end_date__gte=self.date, leave_for='8')
        except:
            try:
                leave = self.user.leaves.get(date=self.date,leave_for='8')
            except:
                leave = False
        return leave        

    @property
    def get_duration(self):
        return self.user_logs_summary.filter(type='in') and time.strftime('%H:%M:%S', time.gmtime(self.user_logs_summary.filter(type='in').values('duration').aggregate(sum=Sum('duration'))['sum'].total_seconds())) or None

    @property
    def get_total_work_duration(self):

        duration = self.get_duration and self.get_duration or "00:00:00"
        try:
            partial_leave = Leave.objects.get(leave_for__in=['6.5','5','2.5','1'], date=self.date, user=self.user)
            if partial_leave.leave_for=="2.5":
                duration = self.sum_of_time([duration, "02:15:00"])
            elif partial_leave.leave_for=="1":
                duration = self.sum_of_time([duration, "01:00:00"])
            elif partial_leave.leave_for=="5":
                duration = self.sum_of_time([duration, "04:30:00"])
            elif partial_leave.leave_for=="6.5":
                duration = self.sum_of_time([duration, "06:45:00"])
        except:
            duration = self.sum_of_time([duration])
        return duration

    @property
    def get_duration_details(self):
        return  self.get_total_work_duration.strftime("%H Hrs %M Min.")

    def saalry_deducated(self):
        from datetime import time
        if self.shift.shift.shift_type == 9:
            half_day,full_day  = time(4,00),time(8,00)
        elif self.shift.shift.shift_type == 10:
            half_day, full_day = time(4,30), time(9,00)
        else:
            return ""

        if self.get_total_work_duration < half_day:
            return self.get_daily_salary and self.get_daily_salary or 0.0
        elif self.get_total_work_duration < full_day :
            return self.get_daily_salary and self.get_daily_salary/2.0 or 0.0
        return ""


    @property
    def get_first_in_time(self):
        return self.user_logs_summary.first() and self.user_logs_summary.first().in_time or None

    @property
    def get_last_out_time(self):
        return self.user_logs_summary.last() and self.user_logs_summary.last().out_time or None

    @property
    def is_fullday(self):
        seconds = self.user_logs_summary.filter(type='in') and self.user_logs_summary.filter(type='in').values('duration').aggregate(sum=Sum('duration'))['sum'].total_seconds() or None        
        if seconds:
            return True if seconds >= 28800 else False
        return False


    @classmethod
    def get_preset_days(cls,user,start_date,end_date):
        holidays = Holidays.objects.filter(date__range=(start_date, end_date),type__in=['1','2']).values_list('date',flat=True)
        present_days = cls.objects.filter(date__range=(start_date,end_date), user = user,user_logs_summary__isnull=False).exclude(date__in=holidays).distinct().count()
        return present_days


    @staticmethod
    def total_user_working_days(cls,user):
        pass

    @staticmethod
    def total_user_working_hours(cls,user):
        pass

class UserAttendanceLogSummary(models.Model):
    attendance_log = models.ForeignKey(UserAttendanceLog, related_name='user_logs_summary')
    in_time = models.TimeField()
    out_time = models.TimeField()
    type = models.CharField(max_length = 10,choices=[('in','In'),('out', 'Out'),('miss_punch','Miss Punch')])
    duration = models.DurationField()
    comment = models.TextField(null=True, blank=True)

class Holidays(models.Model):
    date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=[('1','Holiday'), ('2','WeekOff'),('3','Optional')])
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return ("%s    %s")%(self.description, self.date)

    @staticmethod
    def get_all_sunday_and_odd_suterday(year=2019):
        import calendar
        holidays = []
        for month in range(1,13):
            matrix = calendar.monthcalendar(year,month)
            for index, mat in enumerate(matrix,1):
                if mat[-2]!=0:
                    holidays.append(date(day=mat[-2],month=month,year=year))
                if mat[-1]!=0:
                    holidays.append(date(day=mat[-1],month=month,year=year))
        return holidays

    @classmethod
    def create_weekly_off(cls, year=2020):
        result = cls.get_all_sunday_and_odd_suterday(year=year)
        for dd in result:
            created, res = cls.objects.get_or_create(date=dd, type='2',description="WeekOff")
            print(created, res)

    @classmethod
    def get_holidays(cls, year, month, day, start_days=1):
        print(year, month, day, start_days)
        start_date = date(day=1,month=month,year=year)
        end_date = date(day=day,month=month,year=year)
        return cls.objects.filter(date__range=(start_date,end_date), type__in=['1','2'])


    @classmethod
    def get_holidays_count(cls, year, month, day, start_days=1):
        return cls.get_holidays(year, month, day, start_days).count()



class LeaveCategory(models.Model):
    type=models.IntegerField(choices=LCY)
    total = models.FloatField("total Leave in year")
    user = models.ForeignKey(CustomUser, related_name='leaveconf')
    year = models.ForeignKey(Year, related_name='leaveconf')

    def __str__(self):
        return "%s (%s)"%(self.get_type_display(),self.available)

    @property
    def available(self):
        if self.type==2:
            leaves  = self.leave.filter(date__year=self.year.year).aggregate(total=Coalesce(Sum('leave_count'),0))
            leave = self.total-leaves.get('total',0)
            return leave
        elif self.type==6:
            leaves  = self.leave.filter(date__year=self.year.year).aggregate(total=Coalesce(Sum('leave_count'),0))
            if self.leave.filter(date__month=date.today().month).count()>0:
                return 0
            return self.total-leaves.get('total',0)
        else:
            leaves  = self.leave.filter(date__year=self.year.year).aggregate(total=Coalesce(Sum('leave_count'),0))
            return self.total-leaves.get('total',0)


class Leave(models.Model):
    date = models.DateField()
    shift = models.OneToOneField(EmployeeShift, related_name='leave',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(LeaveCategory, related_name='leave',null=True)
    user = models.ForeignKey(CustomUser, related_name='leaves')
    manager = models.ForeignKey(CustomUser, related_name='leaves_approval',limit_choices_to = {'is_admin': True})
    status = models.IntegerField(max_length=25, default=1, choices=LRS)
    leave_count=models.FloatField(max_length=25, default=1, choices=LRT)
    description = models.TextField("Leave Details")


# class Leave(models.Model):
#     date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     request_date = models.DateTimeField(auto_now_add=True)
#     time = models.TimeField(max_length=10, choices=TIME_SELECT, null=True, blank=True)
#     type = models.CharField(max_length=10, choices=LEAVE_TYPE)
#     leave_for = models.CharField(max_length=10, choices=LEAVE_FOR, default='8')
#     supervisor_approval = models.CharField(max_length=25, default='0', choices=[('0','Waiting for supervisor approval'), ('1','Approved'), ('2','Rejected'),])
#     management_approval = models.CharField(max_length=25, default='0', choices=[('0','Waiting for management approval'), ('1','Approved'), ('2','Rejected'),])
#     status_reason = models.TextField(null=True, blank=True)
#     reject_type = models.CharField(null=True, blank=True, max_length=10, choices=[ ('1','A1'), ('2','A2'), ('3','A3'),])
#     user = models.ForeignKey(CustomUser, related_name='leaves')
#     supervisor = models.ForeignKey(CustomUser, null=True, blank=True, related_name='leaves_approval')
#     description = models.TextField()


#     @classmethod
#     def create_all_user_leave(cls,date,month,year):
#         date = date(year,month,date)
#         for use in CustomUser.objects.filter(parent__isnull=False,date_of_joining__gte=date):
#             cls.objects.create(date=date,request_date=date,type='3',leave_for='8',user=user,supervisor=user.parent,description="added by hr")

#     class Meta:
#         unique_together = ["date", "user", "end_date"]

#     def save(self, *args, **kwargs):
#         from tasks import new_leave_email_notification
#         if not self.pk:
#             self.supervisor = self.user.parent
#             new_leave_email_notification.delay(self.user,self.date)
#         if not self.end_date:
#             self.end_date = self.date
#         return super(Leave, self).save(*args, **kwargs)

#     @property
#     def get_leave_hours(self):
#         if self.leave_for=="2.5":
#             return "02:15:00"
#         elif self.leave_for=="1":
#             return "01:00:00"
#         elif self.leave_for=="5":
#             return "04:30:00"
#         elif self.leave_for=="6.5":
#             return "06:45:00"
#         return "00:00:00"


#     def get_supervisor(self):
#         if self.supervisor:
#             return self.supervisor
#         else:
#             return self.user.parent


#     def get_leave_date(self):
#         if self.end_date == self.date:
#             return  "%s"%(self.date.strftime("%A, %b %d, %Y"))
#         elif self.end_date:
#             return  "%s TO %s"%(self.date.strftime("%A, %b %d, %Y"),self.end_date.strftime("%A, %b %d, %Y"))
#         elif not self.end_date and not self.time:
#             return  self.date.strftime("%A, %b %d, %Y")
#         else:
#             return "%s from %s"%(self.date.strftime("%d %B"), self.time) 

#     def get_status_color(self):
#         if self.supervisor_approval=='0':
#             return "warning"
#         if self.supervisor_approval=='1' and self.management_approval=='0':
#             return "primary"
#         if self.supervisor_approval=='1' and self.management_approval=='1':
#             return "info"
#         if self.reject_type:
#             return "danger"

#     def get_status(self):
#         if self.supervisor_approval=='0':
#             return "Waiting for TL approval"
#         if self.supervisor_approval=='1' and self.management_approval=='0':
#             return "Waiting for HR approval"
#         if self.supervisor_approval=='1' and self.management_approval=='1':
#             return "Approved"
#         elif self.reject_type:
#             return "Rejected with %s"%(self.get_reject_type_display())

#     @classmethod
#     def user_leave_count(cls,user, start_date=None, end_date=None):
#         """
#         this Calculate Full day leave of user
#         """
#         if not start_date and not end_date:
#             start_date, end_date, days = last_month_start_end_date()

#         leave_taken = 0
#         for leave in cls.objects.filter(user = user, leave_for="8", date__range=(start_date, end_date)):
#             if leave.end_date and leave.end_date<=end_date:
#                 total_days = (leave.end_date-leave.date).days+1
#                 holidays = Holidays.objects.filter(type__in=["1","2"],date__range = [leave.date, leave.end_date]).count()
#                 leave_taken = leave_taken+(total_days-holidays)
#             elif leave.end_date and leave.end_date>end_date:
#                 total_days = (end_date-leave.date).days+1
#                 holidays = Holidays.objects.filter(type__in=["1","2"],date__range = [leave.date,end_date]).count()
#                 leave_taken = leave_taken+(total_days-holidays)
#             else:
#                 leave_taken+=1

#         # check leave start date of before month
#         for leave in cls.objects.filter(user = user, leave_for="8", end_date__range=(start_date, end_date)):
#             if leave.date<start_date:
#                 total_days = (start_date-leave.date).days+1
#                 holidays = Holidays.objects.filter(type__in=["1","2"],date__range = [start_date, leave.end_date]).count()
#                 leave_taken = leave_taken+(total_days-holidays)

#         return leave_taken

#     @classmethod
#     def full_day_leave_count(cls, user, start_date=None, end_date=None):
#         """
#         this method is copy of user_leave_count with improvement way
#         """
#         leave_taken = 0 
#         leaves = cls.objects.filter(Q(date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date)), user = user, leave_for="8")
#         for leave in leaves:
#             if leave.end_date:
#                 if leave.end_date<=end_date and leave.date >=start_date:
#                     leave_taken += (leave.end_date-leave.date).days+1
#                     hstart,hend = leave.end_date,leave.date
#                 elif leave.end_date<=end_date and leave.date <=start_date:
#                     leave_taken += (leave.end_date-start_date).days+1
#                     hstart,hend = leave.end_date,start_date

#                 elif leave.end_date>end_date:
#                     leave_taken += (end_date-leave.date).days+1
#                     hstart,hend = end_date,leave.date

#                 elif leave.end_date == leave.date:
#                     leave_taken+=1
#                     hstart,hend = leave.end_date,leave.date

#                 holidays = Holidays.objects.filter(type__in=["1","2"],date__range = [hend,hstart]).count()
#                 leave_taken = leave_taken-holidays

#             elif leave.date:
#               leave_taken+=1
#         return leave_taken


class HubstaffUser(models.Model):
    user = models.OneToOneField(CustomUser, related_name='hubstaf')
    hubstaff_id = models.CharField(max_length=100)

    def __str__(self):
        return '%s, %s' % (self.user, self.hubstaff_id)


class WorkFromHome(models.Model):
    user = models.ForeignKey(CustomUser, related_name='wfh')
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    status = models.CharField(max_length=10, default='1', choices=[('1','pending'), ('2','Acepted'),('3','Rejected')])
    supervisor = models.ForeignKey(CustomUser, related_name='manage_wfh')
    hubstaff_id = models.ForeignKey(HubstaffUser, related_name='manage_wfh',null=True, blank=True)
    def __str__(self):
        return '%s, %s' % (self.user, self.date)

    def save(self, *args, **kwargs):
        super(WorkFromHome, self).save(args, kwargs)

    class Meta:
        unique_together = ('user', 'date')



# class LeaveBank(models.Model):
#     user = models.ForeignKey(CustomUser, related_name='leave_banks')
#     leave_bank = models.FloatField(default=1)
#     created_at = models.DateTimeField(auto_now_add=True)
#     type = models.CharField(max_length=10, default=1, choices=[('1','added'), ('2','Used agains leave')])

#     def __str__(self):
#         return '%s     %s' % (self.user, self.leave_bank)

#     @classmethod
#     def leave_in_bank(cls,user):
#         leave_added = cls.objects.filter(user=user, type="1").count()
#         leave_used = cls.objects.filter(user=user, type="2").count()
#         return leave_added-leave_used
#     @property
#     def get_leave_bank(self):
#         return self.user.leave_bank



@receiver(post_save, sender=Leave)
def leave_post_save(sender, instance, created, *args, **kwargs):
    from attendance.tasks import leave_status_update_email_notification,new_leave_email_notification
    if created:
        new_leave_email_notification.delay(instance)
    else:
        leave_status_update_email_notification.delay(instance)


# @receiver(post_save, sender=EmployeeShift)
# def shift_correction(sender, instance, created, update_fields=None, **kwargs):
#     if created:
#         if instance.date.strftime("%A") in ['Saturday'] and instance.shift.weekday == 5:
#             instance.shift = Shift.weekoff_shift()
#         elif instance.date.strftime("%A") in ['Saturday'] and instance.shift.weekday == 6:
#             holidays = Holidays.get_all_sunday_and_odd_suterday()
#             if instance.date.date() in holidays:
#                 instance.shift = Shift.weekoff_shift()

#         if instance.date.strftime("%A") == 'Sunday':
#             instance.shift = Shift.weekoff_shift()        

#         instance.save()

    # try:
    #     old_instance = Leave.objects.get(id=instance.id)
    #     if old_instance.get_status_color() != instance.get_status_color():
    #         leave_status_update_email_notification.delay(instance)
    # except:
    #     new_leave_email_notification.delay(instance.user,instance.date)
