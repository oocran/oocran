from django import forms
from .models import Scheduler


class SchedulerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SchedulerForm, self).__init__(*args, **kwargs)
        self.fields['destroy'].label = "Delete scheduler once done!"
        self.fields['time'] = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
        self.fields['action'] = forms.ChoiceField(required=False,
                                                widget=forms.Select(attrs={"onChange": 'select(this);'}),
                                                choices=[("Launch", "Launch"),
                                                         ("Shut Down", "Shut Down")])

    class Meta:
        model = Scheduler
        fields = [
            "name",
            "description",
            "action",
            "ns",
            "time",
            "destroy",
        ]