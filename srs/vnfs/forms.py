from django import forms
from .models import Vnf


class VnfForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.images = kwargs.pop('images')
        self.nfs = kwargs.pop('nfs')
        super(VnfForm, self).__init__(*args, **kwargs)
        self.fields['image'] = forms.ChoiceField(required=False, choices=[(x.name, x.name) for x in self.images])
        self.fields['nf'] = forms.MultipleChoiceField(choices=[(x.id, x) for x in self.nfs])
        # self.fields['hpc'] = forms.MultipleChoiceField(choices=[("device1", "device1"),("device2","device2")])
        # self.fields['hpc'].label = "PCI Passthough devices"
        self.fields['min_cpu'].label = "min."
        self.fields['max_cpu'].label = "max."
        self.fields['min_ram'].label = "min."
        self.fields['max_ram'].label = "max."
        self.fields['disc'].label = "Disc (GB)"
        self.fields['nics'].label = "Num. NICs"
        # self.fields['numa'].label = "Number of NUMA nodes"
        self.fields['nf'].label = "Select Network Functions"
        self.fields['real_time'].label = "Run in real time"

    class Meta:
        model = Vnf
        fields = [
            "name",
            "description",
            "image",
            "nf",
            "min_cpu",
            "max_cpu",
            "min_ram",
            "max_ram",
            "disc",
            "nics",
            "real_time",
        ]