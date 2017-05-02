from django import forms
from .models import Vnf


class VnfForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.images = kwargs.pop('images')
        self.nfs = kwargs.pop('nfs')
        super(VnfForm, self).__init__(*args, **kwargs)
        self.fields['image'] = forms.ChoiceField(required=False, choices=[(x.name, x.name) for x in self.images])
        self.fields['nf'] = forms.MultipleChoiceField(choices=[(x.id, x) for x in self.nfs])
        self.fields['create'].label = "Convert into image."

    class Meta:
        model = Vnf
        fields = [
            "name",
            "description",
            "image",
            "nf",
            "create",
        ]