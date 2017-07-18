from django import forms
from .models import Image


class ImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['architecture'] = forms.ChoiceField(required=True,
                                                        choices=[('amd64', 'amd64'),
                                                           ('i386', 'i386')])
        self.fields['format'] = forms.ChoiceField(required=True,
                                                  choices=[('OpenStack', 'OpenStack'),
                                                           ('AMI', 'AMI'),
                                                           ('Docker', 'Docker'), 
                                                           ('Libvirt', 'Libvirt'),
                                                           ('VirtualBox', 'VirtualBox'),
                                                           ('VMware', 'VMware')])

    class Meta:
        model = Image
        fields = [
            "name",
            "version",
            "format",
            "architecture",
        ]
