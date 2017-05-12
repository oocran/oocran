from django import forms
from .models import Nf


class NfForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.libraries = kwargs.pop('libraries')
        super(NfForm, self).__init__(*args, **kwargs)
        self.fields['libraries'] = forms.MultipleChoiceField(choices=[(x.id, x) for x in self.libraries], required=False)

    class Meta:
        model = Nf
        fields = [
            "name",
            "description",
            "script",
            "file",
            "libraries",
            "libraries_order",
        ]
