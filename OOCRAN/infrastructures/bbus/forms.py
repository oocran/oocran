from .models import Utran
from django import forms


class DeploymentForm(forms.ModelForm):

    class Meta:
        model = Utran
        fields = [
            "name",
            "file",
        ]