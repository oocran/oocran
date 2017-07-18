from django import forms
from .models import Ue


class AttachForm(forms.Form):

	def __init__(self, *args, **kwargs):
		self.attached_to = kwargs.pop('pools')
		super(AttachForm, self).__init__(*args, **kwargs)
		self.fields['attached_to'] = forms.ChoiceField(required=False, choices=[(x.id, x.name) for x in self.attached_to])

    	class Meta:
    		model = Ue
    		fields = ["attached_to",]


class UeForm(forms.Form):
    file = forms.FileField()