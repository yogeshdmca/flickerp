from django.db import models
from django.conf import settings
from opportunity.models import Lead


class estimation(models.Model):
	lead = models.ForeignKey(Lead)
	estimation_description = models.TextField(null=True, blank=True)
	assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_created_by", verbose_name="Created By")
	modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_modified_by", verbose_name="Created By")
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
