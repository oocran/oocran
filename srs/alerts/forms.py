from django import forms
from .models import Alert


class AlertForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlertForm, self).__init__(*args, **kwargs)
        self.fields['action'] = forms.ChoiceField(required=False,
                                                  widget=forms.Select(attrs={"onChange": 'select(this);'}),
                                                  choices=[("Launch", "Launch"),
                                                           ("Shut Down", "Shut Down"),
                                                           ("Reconfigure", "Reconfigure"), ])

    class Meta:
        model = Alert
        fields = [
            "name",
            "description",
            "action",
            "script",
        ]