# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import Sum
from django.conf import settings
from opportunity.models import Client
from service.manager import ServiceManager, TimeSheetManager
from service import SERVICE_STATUS
from datetime import date, timedelta
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

SERVICE_TYPE = [
    ('dedicated', "Dedicated"),
    ('hourly', 'Hourly Basic'),
    ('shared', "Shared"),
    ('estimation', "Estimation Basis"),
    ('freetask', "Free  Service"),
]


TIMESHEET_TYPE = [
    ('task', 'Task(Custom)'),
    ('estimation', 'Estimation'),
    ('client', "Client"),
    ('pro_service', "Project/service"),
    ('team', "Team"),
    ('inhouse', "GEITPL-Inhouse"),
    ('learning', "Learning/Training"),
]

FIELD_TYPE = [
    ('user', 'User Model'),
    ('service', 'Service Model'),
    ('clients', 'Clients'),
    ('text', 'Text filed'),
    ('m2m_user', "Many to Many User"),
    ('m2m_service', "Many to Many User")

]

RATING_CHOICES = [
    (1, '$5 - $8 per hour'),
    (2, '$8 - $12 per hour'),
    (3, '$12+ per hour')
]

class TimesheetType(models.Model):
    title = models.CharField("Title", max_length=50)
    type = models.CharField(
        "Timesheet Type", max_length=100, choices=TIMESHEET_TYPE)
    field_type = models.CharField(
        "Timesheet Type", max_length=100, choices=FIELD_TYPE, default='text')

    developer = models.BooleanField(default=True)
    supervisore = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    comment = models.CharField("Title", max_length=100,default="Lower Value is better")
    percentage = models.IntegerField("Performance percenrage of category",default=100)
    css_class = models.CharField("Title", max_length=100, default="bg-muted")
    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField("Service title", max_length=50)
    client = models.ForeignKey(Client, related_name="services")
    type = models.CharField(
        "Services Type", max_length=30, choices=SERVICE_TYPE)
    status = models.CharField(
        "Services Status", max_length=30, choices=SERVICE_STATUS)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField("end date of services", null=True, blank=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="services")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="service_records", null=True, blank=True)
    rating = models.IntegerField("Experience Label Rating", default=1, choices=RATING_CHOICES)
    sudo_name = models.CharField("Dev sudo Name", max_length=50)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='childs')

    objects = ServiceManager()

    def get_start_date(self):
        return self.start_date.date()


    def get_alloted_today(self):

        return self.allotments.filter(date = date.today())

    def get_service_expire_title(self):
        if self.end_date > date.today():
            return "%s days left"%((self.end_date-date.today()).days)
        elif self.end_date == date.today():
            return "Expiring today"
        else:
            return "Expired on %s" %(self.end_date)

    def get_service_expire_colore(self):
        if self.end_date-timedelta(days=6) < date.today() and self.status != 'done': 
            return 'warning'
        elif self.end_date > date.today()+timedelta(days=5) and self.status != 'done':
            return "success"
        elif self.end_date == date.today():
            return "info"
        else:
            return ""



    def get_hours(self):
        if self.type == 'dedicated':
            service_records = self.records.filter(start_date__lte = date.today(), end_date__gte = date.today(),action="1").first()
            service_otp = self.records.filter(start_date__lte = date.today(), end_date__gte = date.today(),action="2")            
            if not service_records:
                return 0.0
            if service_otp:
                hours = sum([otp.per_day for otp in service_otp])
                return service_records.per_day-hours
            else:
                return service_records.per_day

        else:
            total_hours = self.records.filter(
                action='1').aggregate(total=Sum('total_hours'))

            total_otp = self.records.filter(
                action='2').aggregate(total=Sum('total_hours'))
            print (total_otp)
            if total_otp.get('total', 0):
                return total_hours.get('total', 0) - total_otp.get('total', 0)
            else:
                return total_hours.get('total', 0)


    def get_max_show_date(self):
        return date.today() + timedelta(days=7)

    def __str__(self):
        return self.title

    def get_alloted_hours(self):
        total_hours = self.allotments.filter(
            date__gte=self.get_start_date()).aggregate(total=Sum('hours'))
        return total_hours.get('total', 0)

    def get_available_hours(self):
        if self.type == 'dedicated':
            return self.get_hours()

        return self.get_hours() - (self.get_alloted_hours() or 0)

    def get_completed_percentage(self):
        if self.type == 'dedicated':
            return ((date.today() - self.get_start_date()).days + 1) * 100 / ((self.end_date - self.get_start_date()).days + 1)
        else:
            passed_hours = self.allotments.filter(
                date__lt=date.today()).aggregate(total=Sum('hours'))
            return (passed_hours.get('total', 0) or 0) * 100 / self.get_hours()

    @property
    def get_full_name(self):
        return "%s, %s" % (self.title, self.client)


    def get_assined_hours_filled_by_users(self):
        return self.filled.filter(category__isnull=True).values('employee__first_name').annotate(hours_sum=Sum('hours'))

    def get_unassined_hours_filled_by_users(self):
        return self.filled.filter(category__isnull=False).values('employee__first_name',"category__title").annotate(hours_sum=Sum('hours'))


class ServiceRecords(models.Model):
    service = models.ForeignKey(Service, related_name="records")
    start_date = models.DateField("Start Date of service")
    end_date = models.DateField("End Date Of Service")
    status = models.CharField(
        "Services Status", max_length=30, choices=SERVICE_STATUS, default='open')
    title = models.CharField("Service title", max_length=50)
    per_day = models.FloatField("Per Day Hours")
    total_hours = models.FloatField("total Hours of  aggrement")
    action = models.CharField(
        "Services Status", max_length=30, choices=(('1','Added'),('2','Deleted')), default='1'
        )


    def __str__(self):
        return self.service.title

    @property
    def get_hours_details(self):
        if self.service.type == 'dedicated':
            return "%s Hours/Day"%(self.per_day)
        else:
            return "%s Hours"%(self.total_hours)


class ScheduleAllotment(models.Model):
    service = models.ForeignKey(Service, related_name="allotments")
    alloted_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="services_alloted")
    hours = models.FloatField("Hours alloted", null=True, blank=True)
    date = models.DateField("Date")

    # Need to add is this filled by developer or not


    @property
    def description(self):
        return "Timesheet: %s "%(self.hours) 









class TimesheetFiled(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="filled_by")

    category = models.ForeignKey(
        TimesheetType, related_name="timesheets", null=True, blank=True)

    service = models.ForeignKey(
        Service, related_name="filled", null=True, blank=True)

    help_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="filled_tech_helps", null=True, blank=True)

    meeting_with = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="filled_meetings", null=True, blank=True)

    description = models.CharField(
        "What you did ", max_length=200, null=True, blank=True)

    hours = models.FloatField("Hours filled")
    date = date = models.DateField("Date", null=True)


    approve = models.CharField(
        "Timesheet Status", max_length=30, choices=(('new','New'),('approved','Approved'),('rejected','Rejected')
            ))

    approver_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="timesheet_approver", null=True, blank=True)

    objects = TimeSheetManager()

    @property
    def get_hours(self):
        return self.hours

    def get_assined_hours(self):
        try:
            return int(self.service.allotments.get(date=self.date, alloted_to=self.employee).hours)
        except:
            return False

    def get_schedule_allotment(self):
        try:
            return self.service.allotments.get(date=self.date, alloted_to=self.employee)
        except:
            return False
    @property
    def get_display_title(self):
        if self.service:
            title = "%s For %s"%(self.category.title, self.service.title)
            return title

        elif self.meeting_with:
            title = "%s Meeting With %s"%(self.category.title, self.meeting_with.get_full_name)
            return title

        elif self.help_to:
            title = "Doing %s with %s"%(self.category.title, self.help_to.get_full_name)
            return title

        elif self.description:
            title = "%s With Details %s"%(self.category.title, self.description)
            return title


    @property
    def get_suportive(self):

        if self.service:
            return self.service

        elif self.meeting_with:
            return self.meeting_with

        elif self.help_to:
            return self.help_to.get_full_name

        elif self.description:
            return self.description




# singnals For Models in this file

@receiver(pre_delete, sender=ScheduleAllotment)
def schedule_allotment_deleted(sender, instance, **kwargs):
    TimesheetFiled.objects.filter(date=instance.date, service = instance.service, employee=instance.alloted_to).delete()


@receiver(post_save, sender=ServiceRecords)
def schedule_allotment_deleted(sender, instance, **kwargs):
    service = instance.service
    service.end_date = instance.end_date
    service.save()
