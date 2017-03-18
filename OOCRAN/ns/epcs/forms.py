from .models import Epc
from django import forms

'''class EpcForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EpcForm, self).__init__(*args, **kwargs)
        self.fields['graph'].widget = forms.Textarea(attrs={'id': 'code'})
        self.fields['graph'].initial = ''

    class Meta:
        model = Epc
        fields = [
            "name",
            "graph",
        ]'''


class EpcForm(forms.ModelForm):
    vim = forms.CharField(max_length=120)

    def __init__(self, *args, **kwargs):
        super(EpcForm, self).__init__(*args, **kwargs)
        self.fields['vim'] = forms.ChoiceField(required=True,
                                               choices=[('Near', 'Near'), ('Select', 'Select'), ('Local', 'Local')])

    class Meta:
        model = Epc
        fields = [
            "name",
            "vim",
            "file",
        ]
