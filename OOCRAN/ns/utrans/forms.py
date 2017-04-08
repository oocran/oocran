from .models import Utran
from django import forms


class DeploymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DeploymentForm, self).__init__(*args, **kwargs)
        self.fields['vim_option'] = forms.ChoiceField(required=True, choices=[('Near', 'Near'), ('Select', 'Select')])

    class Meta:
        model = Utran
        fields = [
            "name",
            "vim_option",
            "file",
        ]


class DeploymentVagrantForm(forms.ModelForm):
    class Meta:
        model = Utran
        fields = [
            "name",
            "file",
        ]
