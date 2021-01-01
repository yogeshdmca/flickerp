from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Opportunity)
admin.site.register(Lead)
admin.site.register(Client)

admin.site.register(Country)

admin.site.register(OpportunityScheduler)
