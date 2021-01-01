from django.db import models
from django.db.models import Sum, Count, Value
from datetime import date, datetime, timedelta
import calendar
import operator
from sorl.thumbnail import get_thumbnail
from config import week_range

class UserObjectManager(object):

    def get_account_number(self):
        return self.contracts.get(is_active=True).beneficiary_account_number


    def get_thumbnail(self, height=100,witth=100):
        size = "%sx%s"%(height, witth)
        if self.profile_image.url:
            return get_thumbnail(self.profile_image.path, size, crop='center', quality=99).url
        else:
            return "/static/img/user_default.png"
    #get_direct_supervisor
    @property
    def get_direct_supervisor_under_me(self):
        return self.childs.filter(childs__isnull=False).annotate(ids=Count('id'))

    #get_supervisors
    def get_all_supervisors_under_me(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in type(self).objects.filter(parent=self, childs__isnull=False).annotate(ids=Count('id')):
            _r = c.get_all_supervisors_under_me(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    #get_all_childs
    def get_all_childs_under_me(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in type(self).objects.filter(parent=self).annotate(ids=Count('id')):
            _r = c.get_all_childs_under_me(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    #get_all_childs
    def get_all_childs_only(self):
        return self.get_all_childs_under_me(include_self=False)

    def get_parents_lsit(self):
        parent = self.parent
        if parent:
            user_list = [{
                "state": {'opened': 'true'},
                "id": str(parent.pk),
                "parent": parent.parent and str(parent.parent.pk) or '#',
                "text": parent.get_full_name,
                "icon": parent.profile_image and parent.get_thumbnail(44,44) or "glyphicon glyphicon-user"
            }]

            while(parent.parent):
                parent = parent.parent
                parent_dict = {
                    "state": {'opened': 'true'},
                    "id": str(parent.pk),
                    "parent": parent.parent and str(parent.parent.pk) or '#',
                    "text": parent.get_full_name,
                    "icon": parent.profile_image and parent.get_thumbnail(44,44) or "glyphicon glyphicon-user"
                }
                user_list.append(parent_dict)

            return user_list
        return []

    def get_children_for_select_box(self, level=2):
        children = self.childs.all()
        user_list = []
        for child in children:
            if child.is_active:
                child_dict = {
                    "id": str(child.pk),
                    "level": level,
                    "text": child.get_full_name,
                }

                user_list.append(child_dict)
            if child.childs.all():
                temp = level + 1
                user_list = user_list + \
                    child.get_children_for_select_box(level=temp)

        return user_list

    def get_sales_children_for_select_box(self, level=2):
        if self.department == '1':
            children = type(self).objects.filter(department='3')
        else:
            children = self.childs.all().filter(department='3')

        user_list = []
        for child in children:
            if child.is_active:
                child_dict = {
                    "id": str(child.pk),
                    "level": level,
                    "text": child.get_full_name,
                }

                user_list.append(child_dict)
            if child.childs.all():
                temp = level + 1
                user_list = user_list + \
                    child.get_sales_children_for_select_box(level=temp)

        return user_list
        
    def get_child_list(self):
        children = self.childs.all()
        user_list = []
        for child in children:
            if child and child.is_active:
                child_dict = {
                    "state": {'opened': 'true'},
                    "id": str(child.pk),
                    "parent": str(child.parent.pk),
                    "text": child.get_full_name,
                    "icon": child.profile_image and child.get_thumbnail(44,44) or "glyphicon glyphicon-user"
                }

                user_list.append(child_dict)
                if child.childs.all():
                    user_list = user_list + child.get_child_list()

        return user_list

    def get_sub_ordinate(self):
        user_list = []
        if self.parent:
            for child in self.parent.childs.all():
                if child.is_active:
                    child_dict = {
                        "state": {'opened': 'true'},
                        "id": str(child.pk),
                        "parent": str(child.parent.pk),
                        "text": child.get_full_name,
                        "icon": child.profile_image and child.get_thumbnail(44,44) or "glyphicon glyphicon-user"
                    }
                    user_list.append(child_dict)
        else:
            child = self
            if child.is_active:
                child_dict = {
                    "state": {'opened': 'true'},
                    "id": str(child.pk),
                    "parent": '#',
                    "text": child.get_full_name,
                    "icon": child.profile_image and child.get_thumbnail(44,44) or "glyphicon glyphicon-user"
                }
                user_list.append(child_dict)

        return user_list

    @property
    def get_heirarchy(self):
        return self.get_parents_lsit() + self.get_sub_ordinate() + self.get_child_list()

        

    def get_time_sheet_performance(self, month = None, year=None):
        records = []
        from attendance.models import Holidays
        from service.models import TimesheetType

        if not month and not year:
            month = date.today().month
            year = date.today().year
            total_days = date.today().day
        else:
            total_days = calendar.monthrange(year, month)[1]

        holidays = Holidays.get_holidays_count(year, month,total_days)
        working_hours = (total_days-holidays)*8

        if month == 1 and year == 2018:
            working_hours = working_hours-16

        start_date = date(year=year, month=month, day = 1)
        end_date = date(year=year, month=month, day = total_days)

        #print working_hours, total_days, holidays

        hours_services = self.filled_by.filter(date__range=(start_date,end_date), service__isnull=False,category__isnull=True).aggregate(total=Sum('hours'))
        hours_in_services = hours_services.get('total', 0)
        if hours_in_services:
            working_percentage = 100/(working_hours/hours_in_services)
        else:
            working_percentage = 0

        records.append(
                {'type':"Client Task/Project",
                'name':"Assigned Task",'comment':"Higer Value is better",
                'value':working_percentage,
                'color':'bg-success'
                })

        for category in TimesheetType.objects.filter(active=True):
            total_hours = self.filled_by.filter(date__range=(start_date,end_date), category=category,approve=True).aggregate(total=Sum('hours'))
            hours = total_hours.get('total', 0)
            if hours:
                working_percentage = category.percentage/(working_hours/hours)
            else:
                working_percentage=0
            records.append(
                {'type':category.get_type_display,
                'name':category.title,'comment':category.comment,
                'value':working_percentage,
                'color':category.css_class
                })
        total_percentage = sum(map(operator.itemgetter('value'),records))
        return {'records':records, 'total_percentage':total_percentage}

    def weekly_shift(self):
        return self.shifts.filter(date__range=(datetime.now(), datetime.now()+timedelta(days=10))).order_by('date')

    # def date_wise_halfday(self):
    #     from attendance.models import last_month_start_end_date, Holidays
    #     start_date,end_date,total_days = last_month_start_end_date()
    #     holidays = Holidays.objects.filter(date__range=(start_date, end_date),type__in=['1','2']).values_list('date',flat=True)
    #     attendance_logs = self.attendance_logs.filter(date__lte=end_date, date__gte=start_date).exclude(date__in=holidays)
    #     half_days = [log for log in attendance_logs if not log.is_fullday]
    #     return half_days

    # def pending_leave(self):
    #     return self.leaves_approval.filter(supervisor_approval='0').count()

    def pending_timesheet_approval(self):
        from service.models import TimesheetFiled
        return TimesheetFiled.objects.filter(category__isnull=False,approve='new',employee__parent=self).count()
        #return self.timesheet_approver.filter(approve='new').count()