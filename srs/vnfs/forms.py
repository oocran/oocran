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
                                                            #('Azure','Azure'),
                                                            #('AWS','AWS'),
                                                            #('GCE', 'GCE'),
                                                            ("Libvirt", "Libvirt"),
                                                            ("VirtualBox", "VirtualBox"),
                                                            ("Docker", "Docker"),]) 
                                                            #("VMware Fusion","VMware Fusion"),
                                                            #("VMware Workstation","VMware Workstation"),
                                                            #("Paralells", "Paralells"),
                                                            #("Hype-V","Hype-V"),])

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