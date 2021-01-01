# from django import forms
# from django.contrib.auth import get_user_model
# from .models import Department

# class DepartmentCreateForm(forms.ModelForm):

#     class Meta:
#         model = Department
#         exclude = ('created_by', 'modified_by', 'created_at', 'modified_at')
#         widgets = {
#             'name': forms.TextInput(attrs={'class':'form-control', 'required':'true'}),
#         }