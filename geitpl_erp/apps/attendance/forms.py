from django import forms
from .models import Holidays, Leave, EmployeeShift, WorkFromHome
from django.conf import settings
#from config import LEAVE_FOR


LEAVE_FOR = [
    ('8','Full Day(9 hrs)'),
    ('2.5','1/4 day (2 hrs 15 min)'),
    ('1','1 Hour'),
    ]


class HolidayCreateForm(forms.ModelForm):
    class Meta:
        model = Holidays
        exclude = ()


class LeaveCreateForm(forms.ModelForm):
    
    class Meta:
        model = Leave
        exclude = ('user', 'manager', 'status','shift')

    # def __init__(self, *args, **kwargs):
    #     super(LeaveCreateForm,self).__init__(*args,**kwargs)
    #     self.fields['type'].empty_label = None


class WFHCreateForm(forms.ModelForm):
    class Meta:
        model = WorkFromHome
        fields = ('date','hubstaff_id')

    def __init__(self, *args, **kwargs):
        super(WFHCreateForm,self).__init__(*args,**kwargs)

        
class AdministrationLeaveCreateForm(LeaveCreateForm):
    pass

# class LeaveBankForm(forms.ModelForm):
#     class Meta:
#         model = LeaveBank
#         exclude = ('created_by', 'modified_by', 'created_at', 'modified_at','type','leave_bank')