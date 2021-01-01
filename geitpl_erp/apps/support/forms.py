from django import forms
from .models import Ticket
from attachment.models import Attachment
from django.conf import settings

class OpportunityCreateForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        exclude = ('created_by', 'modified_by', 'created_at', 'modified_at')