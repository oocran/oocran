from alerts.models import Alert
from schedulers.models import Scheduler
from django import forms


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


class SchedulerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SchedulerForm, self).__init__(*args, **kwargs)
        self.fields['time'] = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
        self.fields['destroy'].label = "Delete scheduler once done!"
        self.fields['file'].widget.attrs.update({'id': 'Ufile'})
        self.fields['action'] = forms.ChoiceField(required=False,
                                                widget=forms.Select(attrs={"onChange": 'select(this);'}),
                                                choices=[("Launch", "Launch"),
                                                         ("Shut Down", "Shut Down"),
                                                         ("Reconfigure", "Reconfigure")])

    class Meta:
        model = Scheduler
        fields = [
            "name",
            "description",
            "action",
            "time",
            "file",
            "script",
            "destroy",
        ]