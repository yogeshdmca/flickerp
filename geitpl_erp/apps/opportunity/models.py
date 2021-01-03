from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from attachment.models import Attachment
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import date,timedelta

# Create your models here.
communication_type_dict = [
    ('1', 'Skype'),
    ('2', 'Drop a Email'),
    ('3', 'Phone Call'),
    ('4', 'Linkedin'),
    ('5', 'Facebook'),
    ('6', 'Whatsapp'),
    ('7', 'Other'),
]

PROSPECT_STATUS = (
        ('1','New'),
        ('2', "Positive Response"),
        ('3', "Hot Prospect"),
        ('4', "converted to Lead"),
        ('5', "Not Intrested"),
        ('6', "No Response"),
        ('111','Created by Website'),
    )


LEAD_STATUS = (
        ('1','New'),
        ('2', "Positive Response"),
        ('3', "Hot Prospect"),
        ('4', "converted to Project"),
        ('5', "Not Intrested"),
        ('6', "No Response"),
        ('111','Created by Website'),
    )

LEAD_SOURCE =  (
    ('1', 'Website'),
    ('2', 'Email Marketing'),
    ('3', 'Client Reference'),
    ('4', 'Linkedin'),
    ('5', 'Facebook'),
    ('6', 'Whatsapp'),
    ('7', 'Clutch'),
    ('8', 'Craigslist'),
    ('9', 'Other'),
)


SCHEDULE_STATUS =  (
        ('0', "Mark as Lead"),
        ('1', "Next call"),
        ('2', "Lose"),
        ('3', "No Response"),
        ('4', "complted"),
    )

SCHEDULE_RESULT = SCHEDULE_STATUS



class Country(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Client(models.Model):
    client_name = models.CharField(max_length=100)
    client_comapny = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    skype = models.CharField(max_length=50, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    country = models.ForeignKey(Country, related_name='clients',null=True, blank=True)
    def __str__(self):
        return self.client_name or ''


class CreatedandByBaseAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=1, choices=LEAD_SOURCE, default='1')

    class Meta:
        abstract = True



    

class Opportunity(CreatedandByBaseAbstract):
    firstname = models.CharField(max_length=200, null=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    skype = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=70, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    country = models.ForeignKey(Country, related_name='prospects',null=True, blank=True)
    status = models.CharField(max_length=4, choices=PROSPECT_STATUS,default='1')
    description = models.TextField("Project Details",null=True, blank=True,help_text="its can be project or client detail")

    attachments = GenericRelation(Attachment, object_id_field='object_id', content_type_field='content_type', related_query_name='%(app_label)s_%(class)s_content_object')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s", null=True)

    def __str__(self):
        return str(self.firstname)
        
    # class Meta:
    #     unique_together = ['email', 'email']

    @property
    def latest_schedule(self):
        return self.scheduler.last()


    def get_color(self):
        if self.latest_schedule.result=="1" and self.latest_schedule.call_schedule.date() == date.today() : 
            return 'pink'
        elif self.latest_schedule.result=="1" and self.latest_schedule.call_schedule.date() < date.today():
            return 'red'
        elif self.latest_schedule.result=="1" and self.latest_schedule.call_schedule.date() < date.today()+timedelta(days=10):
            return '#f8ad16'
        else:
            return ''


class Scheduler(models.Model):
    communication_type = models.CharField("Mediam of communication",max_length=20, choices=communication_type_dict)
    description = models.TextField("Client communication Details",null=True, blank=True)
    result = models.CharField("Result of Last call",max_length=1, choices=SCHEDULE_RESULT,default='1')
    call_schedule = models.DateTimeField("Next schedule Date if any", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class OpportunityScheduler(Scheduler):
    opportunity = models.ForeignKey(Opportunity, related_name='scheduler')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s", null=True)


class Lead(CreatedandByBaseAbstract):
    client = models.ForeignKey(Client, null=True, blank=True, related_name='lead_client_detail')
    opportunity = models.ForeignKey(Opportunity, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    estimated_price = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=4, choices=LEAD_STATUS,default='1')
    attachments = GenericRelation(Attachment, object_id_field='object_id', content_type_field='content_type', related_query_name='%(app_label)s_%(class)s_content_object')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s", null=True)

    def __str__(self):
      return self.client and self.client.client_name or "No client name"

    @property
    def latest_schedule(self):
        return self.scheduler.last()

class LeadScheduler(Scheduler):
    lead = models.ForeignKey(Lead, null=True, blank=True, related_name='scheduler')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s", null=True)


@receiver(post_save, sender=Opportunity)
def opportunity_created(sender, instance, created,  update_fields=None, **kwargs):
    from attendance.tasks import opportunity_created_email_notification
    if created and instance.status == '111':
        opportunity_created_email_notification.delay(instance)

@receiver(post_save, sender=OpportunityScheduler)
def opportunity_schedulercreated(sender, instance, created,  update_fields=None, **kwargs):
    schedulers = instance.opportunity.scheduler.all().exclude(pk=instance.pk)
    schedulers.update(result='4')
