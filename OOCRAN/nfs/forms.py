from django import forms
from .models import Nf


class NfForm(forms.ModelForm):
    type = forms.CharField(max_length=32)

    def __init__(self, *args, **kwargs):
        super(NfForm, self).__init__(*args, **kwargs)
        self.fields['type'] = forms.ChoiceField(required=False,
                                                widget=forms.Select(attrs={"onChange": 'select(this);'}),
                                                choices=[("file", "file"), ("script", "script"), ("ansible", "ansible"),
                                                         ("puppet", "puppet")])

    class Meta:
        model = Nf
        fields = [
            "name",
            "description",
            "script",
            "file",
            "type",
            "dependencies",
        ]
