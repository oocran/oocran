from .models import Utran, UE
from django import forms


class DeploymentForm(forms.ModelForm):
    class Meta:
        model = Utran
        fields = [
            "name",
            "file",
        ]


class UEForm(forms.Form):
    file = forms.FileField()