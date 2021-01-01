from dashboard.views import landingpage
from user.views.common import login
from django.shortcuts import redirect
import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from attendance.models import Leave


class LoginMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.required = tuple(re.compile(url)
                              for url in settings.LOGIN_REQUIRED_URLS)
        self.exceptions = tuple(re.compile(url)
                                for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def __call__(self, request):
        if request.user.is_authenticated():
            user = request.user
            request.role = 'admin'
            if user.is_admin or user.department == '1':
                request.profile = request.user
                request.role = 'admin'
            elif user.department == '2':
                request.profile = request.user
                request.role = 'development'
            elif user.department == '3':
                request.profile = request.user
                request.role = 'sales'
            elif user.department == '4':
                request.profile = request.user
                request.role = 'humanresource'

        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # No need to process URLs if user already logged in
        for url in self.exceptions:
            if url.match(request.path):
                return None

        if request.user.is_authenticated():
            print(request.role, request.path)
            
            # Password change every month
            # if not request.user.password_date or (date.today() - request.user.password_date) > timedelta(days=30):
            #     print "dfffffffffffffffffffffffffffffffffffff"
            #     return redirect("user:change-password")
            
            # Leave not approve till 1st of month
            if request.role == 'admin':
                redirect_url = '/administration/leave/approve/'
                redirect_to = "attendance:approve-leave"
            else:
                redirect_url = '/development/leave/approve/'
                redirect_to = "attendance:development-approve-leave"
#            if request.user.leave_approve > 0 and date.today() == date.today().replace(day=1) and request.path != redirect_url:
 #               return redirect(redirect_to)

            # Timsheet not fill continue 3 days
            # if request.role != 'admin' and request.role != 'humanresource' and request.user.filled_by.last():
            #     if date.today() - request.user.filled_by.last().date > date.today().replace(day=6) - date.today().replace(day=3) and request.path != '/employee/timehseet/':
            #         if request.path == '/employee/fill_timesheet/' or request.path == '/employee/get_timesheet_type_line/' or request.path ==  '/employee/get_timesheet_category_type/' or request.path ==  '/employee/get_timesheet_sub_category_type/' or request.path ==  '/employee/add_new_timesheet_record/':
            #             return None
            #         else:
            #             return redirect('service:timehseet')

            if re.compile(r'/administration/(.*)$').match(request.path) and request.role == 'admin':
                return None
            if re.compile(r'/development/(.*)$').match(request.path) and request.role in ['development','admin']:
                return None
            if re.compile(r'/employee/(.*)$').match(request.path) and request.role in ['development','admin','sales','humanresource']:
                return None

            if re.compile(r'/admin/(.*)$').match(request.path) and request.role in 'admin':
                return None
            if re.compile(r'/sales/(.*)$').match(request.path) and request.role in ['sales','admin']:
                return None
            if re.compile(r'/humanresource/(.*)$').match(request.path) and request.role in ['humanresource','admin']:
                return None
            if re.compile(r'/media/(.*)$').match(request.path):
                return None
            return landingpage(request, *view_args, **view_kwargs)
        return login(request)
