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
from .models import Image


class ImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['architecture'] = forms.ChoiceField(required=True,
                                                        choices=[('amd64', 'amd64'),
                                                           ('i386', 'i386')])
        self.fields['format'] = forms.ChoiceField(required=True,
                                                    widget=forms.Select(attrs={"onChange": 'select(this);'}),
                                                    choices=[('OpenStack', 'OpenStack'),
                                                            ('Azure','Azure'),
                                                            ('AWS','AWS'),
                                                            ('GCE', 'GCE'),
                                                            ("Libvirt", "Libvirt"),
                                                            ("VirtualBox", "VirtualBox"),
                                                            ("Docker", "Docker"),])

    class Meta:
        model = Image
        fields = [
            "name",
            "version",
            "format",
            "architecture",
        ]
