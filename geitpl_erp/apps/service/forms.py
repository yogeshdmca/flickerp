from django import forms
from service.models import ScheduleAllotment


class DateInput(forms.DateInput):
    input_type = 'date'


class ScheduleAllotmentForm(forms.ModelForm):
    hours = forms.ChoiceField(choices=[(x, x) for x in range(1, 9)])

    class Meta:
        model = ScheduleAllotment
        fields = ('alloted_to', 'hours', 'date')
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form-control date', }),
        }

    def __init__(self, user, *args, **kwargs):
        super(ScheduleAllotmentForm, self).__init__(*args, **kwargs)
        self.fields['alloted_to'].choices = [(child.id, child.get_full_name) for child in user.get_all_childs_under_me()] + [(user.id, user.get_full_name)]
