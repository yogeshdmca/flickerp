from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from attachment.models import Attachment
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from sorl.thumbnail import get_thumbnail

from user.models import Skill


related_to_choices = [('1', 'Human Resource'),
					('2', 'Hardware/Software'),
					('3', ''),
					('4', 'Others'),]

ticket_status_choices = [('1', 'Open'),
					('2', 'In Progress'),
					('3', 'Resolved')]



class Industry(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Ticket(models.Model):
    related_to = models.CharField(max_length=10, choices=related_to_choices)
    status = models.CharField(max_length=10, choices=ticket_status_choices)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ticket_created_by", verbose_name="Created By")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ticket_modified_by", verbose_name="Modified By")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ticket_assigned_to")
    attachments = GenericRelation(Attachment, object_id_field='object_id', content_type_field='content_type', related_query_name='%(app_label)s_%(class)s_content_object')

class Portfolio(models.Model):
    title = models.CharField(max_length=100)
    # description = models.Text(max_length=10, choices=ticket_status_choices)
    description = models.TextField()
    skills = models.ManyToManyField(Skill)
    industry = models.ManyToManyField(Industry)
    cover = models.ImageField(upload_to = 'portfolio/')
    developer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="portfolios")
    estimated_hours = models.IntegerField(null=True, blank=True)
    taken_hours = models.IntegerField(null=True, blank=True)
    client = models.CharField(max_length=100,null=True, blank=True)
    live_url = models.URLField(max_length=250,null=True, blank=True)
    attachments = GenericRelation(Attachment, object_id_field='object_id', content_type_field='content_type', related_query_name='%(app_label)s_%(class)s_content_object')

    def __str__(self):
        return self.title

    def get_thumbnail(self, height=60,witth=75):
        size = "%sx%s"%(witth,height)
        if self.cover.url:
            return get_thumbnail(self.cover.path, size, crop='center', quality=99).url
        else:
            return "/static/img/user_default.png"

    def get_skills(self):
        import pdb;pdb.set_trace()
        
        return self.skills
            
