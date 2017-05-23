from django import forms
from .models import Vim, Device
from images.models import Image


class VimForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(VimForm, self).__init__(*args, **kwargs)
        self.fields['type'] = forms.ChoiceField(required=True,
                                                choices=[('OpenStack', 'OpenStack')])

    class Meta:
        model = Vim
        fields = [
            "type",
            "name",
            "ip",
            "latitude",
            "longitude",
            "username",
            "password",
            "password_confirmation",
            "project_domain",
            "project",
            "domain",
        ]


class DeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.node = kwargs.pop('node')
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['node'] = forms.ChoiceField(required=False,
                                                choices=[(x.hypervisor_hostname, x.hypervisor_hostname) for x in
                                                         self.node])

    class Meta:
        model = Device
        fields = [
            "name",
            "node",
            "vendor_id",
            "product_id",
        ]


class ImageForm(forms.ModelForm):
    file = forms.CharField(max_length=300)

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['format'] = forms.ChoiceField(required=True,
                                                  choices=[('iso', 'ISO - Optical Disk Image'),
                                                           ('ova', 'OVA - Open Virtual Appliance'),
                                                           ('qcow2', 'QCOW2 - QEMU Emulator'),
                                                           ('raw', 'Raw'),
                                                           ('vdi', 'VDI - Virtual Disk Image'),
                                                           ('vhd', 'VHD - Virtual Hard Disk'),
                                                           ('aki', 'AKI - Amazon Kernel Image'),
                                                           ('ami', 'AMI - Amazon Machine Image'),
                                                           ('ari', 'ARI - Amazon Ramdisk Image'),
                                                           ('docker', 'Docker')])

    class Meta:
        model = Image
        fields = [
            "name",
            "file",
            "format",
        ]