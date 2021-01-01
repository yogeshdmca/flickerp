from django import forms
from .models import Contract as EmployeeContract
from user.models import CustomUser
from django.conf import settings

class ContractCreateForm(forms.ModelForm):

    class Meta:
        model = EmployeeContract
        exclude = ('created_by', 'modified_by', 'created_at', 'modified_at','expiry_date','is_active')

    def __init__(self, *args, **kwargs):
        super(ContractCreateForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.all().exclude(parent__isnull=True)
