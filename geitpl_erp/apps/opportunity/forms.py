from django import forms
from .models import Opportunity, Lead, OpportunityScheduler, LeadScheduler, Client
from attachment.models import Attachment
from django.conf import settings

class OpportunityCreateForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        exclude = ('user', 'created_at', 'modified_at')


class OpportunityCreateFormAPI(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ('description', 'firstname', 'company_name','skype', 'email', 'contact')


class LeadCreateForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ('created_by', 'modified_by', 'created_at', 'modified_at')  


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('created_by', 'modified_by', 'created_at', 'modified_at')


class AttachmentCreateForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('document',)


class OpportunitySchedulerForm(forms.ModelForm):
    call_schedule = forms.DateTimeField(input_formats=settings.DATETIME_INPUT_FORMATS)
    class Meta:
        model = OpportunityScheduler
        exclude = ('created_by', 'modified_by', 'created_at', 'modified_at', 'opportunity', 'client')


class LeadSchedulerForm(forms.ModelForm):
    call_schedule = forms.DateTimeField(input_formats=settings.DATETIME_INPUT_FORMATS)
    class Meta:
        model = LeadScheduler
        exclude = ('created_by', 'modified_by', 'created_at', 'modified_at', 'description', 'result', 'lead', 'client')