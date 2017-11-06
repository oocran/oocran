"""
    Open Orchestrator Cloud Radio Access Network

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

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
    def __init__(self, *args, **kwargs):
        super(OperatorForm, self).__init__(*args, **kwargs)

    password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=4, widget=forms.PasswordInput)
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
