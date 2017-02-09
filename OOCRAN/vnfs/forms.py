from django import forms
from .models import Vnf


class VnfForm(forms.ModelForm):
    #def __init__(self, *args, **kwargs):
        #self.images = kwargs.pop('images')
        #super(VnfForm, self).__init__(*args,**kwargs)
        #self.fields['image'] = forms.ChoiceField(required=False, choices=[(x, x) for x in self.images])

    class Meta:
        model = Vnf
        fields = [
            "name",
            "description",
            "cpu",
            "ram",
            "disk",
            #"image",
            "script",
            #"interfaces"
        ]
