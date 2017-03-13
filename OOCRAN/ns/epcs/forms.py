from .models import Epc
from django import forms


class EpcForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EpcForm, self).__init__(*args, **kwargs)
        self.fields['graph'].widget = forms.Textarea(attrs={'id': 'code'})
        self.fields['graph'].initial = ''

    class Meta:
        model = Epc
        fields = [
            "name",
            "graph",
        ]
