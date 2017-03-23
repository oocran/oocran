from .models import Utran
from django import forms


class DeploymentForm(forms.ModelForm):
    vim = forms.CharField(max_length=120)

    def __init__(self, *args, **kwargs):
        super(DeploymentForm, self).__init__(*args, **kwargs)
        self.fields['vim'] = forms.ChoiceField(required=True, choices=[('Near', 'Near'), ('Select', 'Select')])

    class Meta:
        model = Utran
        fields = [
            "name",
            "vim",
            "file",
        ]


class DeploymentVagrantForm(forms.ModelForm):
    class Meta:
        model = Utran
        fields = [
            "name",
            "file",
        ]
