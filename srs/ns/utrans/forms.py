from .models import Utran, UE
from django import forms


class DeploymentForm(forms.ModelForm):
    class Meta:
        model = Utran
        fields = [
            "name",
            "file",
        ]


class UEForm(forms.ModelForm):
    class Meta:
        model = UE
        fields = [
            "name",
            "latitude",
            "longitude",
            "sensibility",
            "service",
        ]