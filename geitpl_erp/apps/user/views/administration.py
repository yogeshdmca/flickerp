from django.shortcuts import render
from user.forms import UserLoginForm, SkillCreateForm, FamilyMemberForm,UserCreateForm
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from datetime import datetime, date, time, timedelta
from django.views.generic import View, ListView, DeleteView, CreateView
from django.core.urlresolvers import reverse, reverse_lazy
from user.models import *
# from attendance.models import LeaveBank
from django.template.loader import render_to_string

# Create new User
class AdministrationUserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'users/administration/user_create.html'
    success_url = reverse_lazy('user:users')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        form.instance.is_active = True
        form.instance.is_staff = True
        form.instance.full_name = "%s %s"%(form.instance.first_name, form.instance.last_name)
        form.instance.set_password('geitpl@#$123')
        return super(AdministrationUserCreateView, self).form_valid(form)


# List Users
class AdministrationUserListView(ListView):
    model = CustomUser
    queryset = CustomUser.objects.all().order_by('date_of_joining')
    paginate_by = 50
    template_name = 'users/administration/user_listing.html'


class AdministrationSkillCreateView(CreateView):
    form_class = SkillCreateForm
    template_name = 'users/administration/skill_create.html'
    success_url = reverse_lazy('user:skill-create')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super(AdministrationSkillCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AdministrationSkillCreateView, self).get_context_data(**kwargs)
        context['skills'] = Skill.objects.all()
        return context


class AdministrationFamilyMemberCreateView(CreateView):
    form_class = FamilyMemberForm
    template_name = 'users/partials/family_member_form.html'
    success_url = reverse_lazy('user:users')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        response = super(AdministrationFamilyMemberCreateView, self).form_valid(form)
        if self.request.is_ajax():
            return JsonResponse({'success':1})
        return response


    def form_invalid(self, form):
        if self.request.is_ajax():
            html = render_to_string('users/partials/family_member_form.html', {'fm_form':form}, request=self.request)
            return JsonResponse({'html':html, 'success':0})
        return super(AdministrationFamilyMemberCreateView, self).form_invalid(form)

