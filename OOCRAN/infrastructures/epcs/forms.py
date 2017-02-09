from .models import NVFI
from django import forms


class GUIForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GUIForm, self).__init__(*args,**kwargs)
        self.fields['graph'].widget = forms.Textarea(attrs={'id': 'code'})
        self.fields['graph'].initial = ''

    class Meta:
        model = NVFI
        fields = [
            "name",
            "graph",
        ]