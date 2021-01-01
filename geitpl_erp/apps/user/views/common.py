from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse, Http404
from django.contrib.auth import authenticate, login as user_login
from django.contrib import messages
from django.views.generic import TemplateView
from django.views import View
from django.core.urlresolvers import reverse
from user.forms import UserLoginForm, ChangePasswordForm
from user.models import *
from django.contrib.auth import logout
from datetime import date

# Create your views here.
def login(request):
    next_url = request.GET.get('next',False)
    if request.user.is_authenticated():
        return HttpResponseRedirect("/dashboard/")

    form = UserLoginForm()
    if request.method=='POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username'].lower()
            password = request.POST['password']
            new_user = authenticate(username=username, password=password)

            if new_user is not None:
                if new_user.is_active:
                    user_login(request, new_user)

                    if next_url:
                        return HttpResponseRedirect(next_url)
                    else:
                        return HttpResponseRedirect(reverse("dashboard:dashboard"))
                else:
                    messages.warning(request, 'Your account is not activeted, please activate your account!')
            else:
                messages.warning(request, 'Login email and password are incorrect!!')
                
    return render(request, "users/login.html",{'form':form, 'next':next_url})


def login_as_other(request,userid):
    #if request.user.is_authenticated() and request.user.is_superuser:
    new_user = CustomUser.objects.get(email=userid)
    user_login(request, new_user)
    return HttpResponseRedirect("/")
    #else:
    #    raise Http404


class UserProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['family'] = FamilyMember.objects.filter( user_id=self.request.user.id )
        return context


class ChangePassword(View):
    template_name = "users/change_password.html"
    def get(self, request, *arg, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *arg, **kwargs):
        user = request.user
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if form.check_password(user):
                user.set_password(form.cleaned_data["password2"])
                user.password_date = date.today()
                user.save()
                
                logout(request)
                return HttpResponseRedirect(reverse("user:login"))
            else:
                password_error = "Incorrect Old Password"
        else:
            password_error = "Password and Confirm Password Should be Same."

        return render(request, self.template_name, {"form": form,'password_error':password_error })



def show_salary_password_confirm(request):
    if request.method=="POST":
        password = request.POST.get('confirm_password', '')
        if request.user.check_password(password):
            return render(request, 'users/partials/salary_pay_slip.html', {})
    return JsonResponse({'error':"1", 'msg':'password not valid'})