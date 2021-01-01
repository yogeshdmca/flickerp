from django.shortcuts import render
from user.forms import UserLoginForm, SkillCreateForm, FamilyMemberForm, UserCreateForm
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.contrib.auth import get_user_model, authenticate, login as user_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from datetime import datetime, date, time, timedelta
from django.views.generic import View, ListView, DeleteView, CreateView
from django.core.urlresolvers import reverse, reverse_lazy
from user.models import *
# from attendance.models import LeaveBank
from django.template.loader import render_to_string


from user.views import administration


class HrUserCreateView(administration.AdministrationUserCreateView):
    #template_name = 'users/hr/user_create.html'
    success_url = reverse_lazy('user:hr-users')



# Create new User
class HrUserListView(administration.AdministrationUserListView):
    #template_name = 'users/hr/user_listing.html'
    pass




class HrSkillCreateView(administration.AdministrationSkillCreateView):
    form_class = SkillCreateForm
    #template_name = 'users/hr/skill_create.html'
    success_url = reverse_lazy('user:hr-skill-create')


