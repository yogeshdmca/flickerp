# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Year(models.Model):
    start = models.DateField()
    end = models.DateField()
    year = models.IntegerField("Year Name", unique = True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.start)
        

class FiscalYear(models.Model):
    start = models.DateField("Start Date")
    end = models.DateField("end Date")
    title = models.CharField("Title",max_length=100)
    is_open = models.BooleanField(default=True)
    class Meta:
        unique_together = ('start', 'end',)