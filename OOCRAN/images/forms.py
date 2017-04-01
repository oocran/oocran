from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    file = forms.CharField(max_length=300)

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['format'] = forms.ChoiceField(required=True,
                                                  choices=[('iso', 'ISO - Optical Disk Image'),
                                                           ('ova', 'OVA - Open Virtual Appliance'),
                                                           ('qcow2', 'QCOW2 - QEMU Emulator'), ('raw', 'Raw'),
                                                           ('vdi', 'VDI - Virtual Disk Image'),
                                                           ('vhd', 'VHD - Virtual Hard Disk'),
                                                           ('aki', 'AKI - Amazon Kernel Image'),
                                                           ('ami', 'AMI - Amazon Machine Image'),
                                                           ('ari', 'ARI - Amazon Ramdisk Image'), ('docker', 'Docker')])

    class Meta:
        model = Image
        fields = [
            "name",
            "file",
            "format",
        ]
