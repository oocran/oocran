from django import forms
from .models import Nf


class NfForm(forms.ModelForm):
    class Meta:
        model = Nf
        fields = [
            "name",
            "description",
            "code",
            "script",
        ]
