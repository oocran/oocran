from django import forms
from .models import VIM
from operators.models import Operator


class VIMForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = VIM
        fields = [
            "name",
            "ip",
            "latitude",
            "longitude",
            "username",
            "password",
            "password_confirmation",
            "project_domain",
            "project",
            "domain",
        ]


class CredentialsForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = Operator
        fields = [
            "name",
            "password",
            "password_confirmation",
        ]