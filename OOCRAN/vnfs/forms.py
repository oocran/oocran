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

from django import forms
from .models import Vnf


class VnfForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.images = kwargs.pop('images')
        self.scripts = kwargs.pop('scripts')
        self.key = kwargs.pop('key')
        super(VnfForm, self).__init__(*args, **kwargs)
        self.fields['image'] = forms.ChoiceField(required=False, choices=[(x.name, x.name +' - '+ x.format) for x in self.images])
        self.fields['key'] = forms.ChoiceField(required=False, choices=[(x.id, x) for x in self.key])
        self.fields['scripts'] = forms.MultipleChoiceField(choices=[(x.id, x) for x in self.scripts], required=False)
        self.fields['disc'].label = "Disc (GB)"
        self.fields['provider'] = forms.ChoiceField(required=True,
                                                    widget=forms.Select(attrs={"onChange": 'select(this);'}),
                                                    choices=[('OpenStack', 'OpenStack'),
                                                            ('Azure','Azure'),
                                                            ('AWS','AWS'),
                                                            ('GCE', 'GCE'),
                                                            ("Libvirt", "Libvirt"),
                                                            ("VirtualBox", "VirtualBox"),
                                                            ("Docker", "Docker"),])

    class Meta:
        model = Vnf
        fields = [
            "name",
            "description",
            "image",
            "cpu",
            "ram",
            "disc",
            "key",
            "provider",
            "launch_script",
            "scripts",
            "scripts_order",
        ]