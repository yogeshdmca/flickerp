from django.db import models
from django.conf import settings
# Create your models here.
status_choices = [('1', 'High'),
                    ('2', 'Avarage'),
                    ('3', 'low')]

class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", verbose_name="Created By")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=status_choices)

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.created_at, now)