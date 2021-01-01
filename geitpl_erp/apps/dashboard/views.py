from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, DeleteView
from user.models import CustomUser
from attendance.models import Leave
from django.contrib.sessions.models import Session
from datetime import datetime
import json

# Create your views here.
def landingpage(request):
    user = request.user
    if not user.is_authenticated():
        return redirect("user:login")
    else:
        if user.is_admin or user.department == '1':
            return redirect("dashboard:dashboard")
        elif user.department in ['2', '5', '6', '7']:
            return redirect("dashboard:development-dashboard")
        elif user.department == '3':
            return redirect("dashboard:sales-dashboard")
        elif user.department == '4':
            return redirect("dashboard:hr-dashboard")


class Dashboard(View):
    template_name = 'dashboard/administration.html'
    def get(self, request):
        leave_count = Leave.objects.filter(user__in = self.request.user.childs.all(),status=1).count()
        
        return render(request,self.template_name,{'listofusers':json.dumps(request.user.get_heirarchy),'leave_count':leave_count})
