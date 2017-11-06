"""
    Open Orchestrator Cloud Radio Access Network

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

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