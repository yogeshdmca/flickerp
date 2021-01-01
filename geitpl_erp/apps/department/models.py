# from django.db import models
# from django.conf import settings

# class Department(models.Model):
# 	name = models.TextField()
# 	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_created_by", verbose_name="Created By")
# 	modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_modified_by", verbose_name="Modified By")
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	modified_at = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return self.name