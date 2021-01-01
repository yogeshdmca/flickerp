from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser, Skill, FamilyMember, TlFeedback
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AdminPasswordChangeForm

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = "__all__"

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = "__all__"


class UserLoginForm(forms.Form):
    username = forms.EmailField(max_length=100, label="", required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))


class UserCreateForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(UserCreateForm, self).__init__(*args, **kwargs)
    #     self.fields['agent'].queryset = self.fields['agent'].queryset.filter(client__isnull=False)

    class Meta:
        model = CustomUser
        exclude = ('created_by', 'modified_by', 'created_at', 'modified_at', 'password')
        

class SkillCreateForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ('created_by', 'modified_by', 'created_at', 'modified_at')


class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        exclude = ('created_by', 'modified_by', 'created_at', 'modified_at')


class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(max_length=140, widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)
    password1 = forms.CharField(max_length=140, widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)
    password2 = forms.CharField(max_length=140, widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 == password2:
            return password2
        raise forms.ValidationError("Password and Confirm Password Should Same.")

    def clean_oldpassword(self):
        oldpassword = self.cleaned_data["oldpassword"]
        if not oldpassword:
            raise forms.ValidationError("Enter Your Current Password")
        return oldpassword

    def check_password(self,user):
        is_password = user.check_password(self.cleaned_data["oldpassword"])
        return is_password and True or False

class TlFeedbackForm(forms.ModelForm):
    class Meta:
        model = TlFeedback
        fields = ('positive', 'negative', 'suggestion', 'rating')