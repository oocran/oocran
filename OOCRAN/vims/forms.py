from django import forms
from .models import VIM
from operators.models import Operator


class VIMForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(VIMForm, self).__init__(*args, **kwargs)
        self.fields['type'] = forms.ChoiceField(required=True,
                                                choices=[('OpenStack', 'OpenStack'), ('Vagrant', 'Vagrant')])

    class Meta:
        model = VIM
        fields = [
            "type",
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