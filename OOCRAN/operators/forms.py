from .models import Operator
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class ChangeCredenForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password_confirmation",
        ]


class OperatorForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=32, widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Operator
        fields = [
            "name",
            "password",
            "password_confirmation",
            "email",
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
