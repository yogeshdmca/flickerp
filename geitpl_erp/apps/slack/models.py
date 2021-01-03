from django.db import models
from django.conf import settings

# Create your models here.
class FamilyMember(models.Model):
	id = models.CharField(max_length=140)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='slack')
    display_name = models.CharField(max_length=500)
    real_name_normalized = models.CharField(max_length=500)