from django import forms
from .models import Scenario


class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            "name",
            "description",
            "latitude",
            "longitude",
            "file",
        ]