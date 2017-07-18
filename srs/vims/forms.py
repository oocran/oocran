from django import forms
from .models import Vim, Device
from images.models import Image


class VimForm(forms.Form):
    name = forms.CharField(max_length=32)
    type = forms.ChoiceField(required=True,widget=forms.Select(attrs={"onChange": 'select(this);'}), choices=[('OpenStack', 'OpenStack'),('Azure','Azure'),('AWS','AWS'),('GCE', 'GCE')])
    version = forms.ChoiceField(required=True,widget=forms.Select(attrs={"onChange": 'select(this);'}), choices=[('2', 'Mitaka'),('3','Newton')])

    ip = forms.CharField(max_length=32, initial="controller")
    sdn_controller = forms.CharField(max_length=32,required = False)
    latitude = forms.FloatField(initial=41.40649)
    longitude = forms.FloatField(initial=2.0787274)
    #OpenStack
    username = forms.CharField(max_length=120,required = False)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput,required = False)
    password_confirmation = forms.CharField(max_length=32, widget=forms.PasswordInput, required = False)
    project_domain = forms.CharField(max_length=120,required = False, initial='default')
    project = forms.CharField(max_length=120,required = False, initial='admin')
    public_network = forms.CharField(max_length=120,required = False, initial='provider')
    domain = forms.CharField(max_length=120,required = False, initial='default')
    #AWS
    access_key_id = forms.CharField(max_length=120,required = False)
    secret_access_key = forms.CharField(max_length=120,required = False)
    session_token = forms.CharField(max_length=120,required = False)
    keypair_name = forms.CharField(max_length=120,required = False)
    #Azure
    tenant_id = forms.CharField(max_length=120,required = False)
    client_id = forms.CharField(max_length=120,required = False)
    client_secret = forms.CharField(max_length=120,required = False)
    subscription_id = forms.CharField(max_length=120,required = False)
    #GCE
    google_project_id = forms.CharField(max_length=120,required = False)
    google_client_email = forms.CharField(max_length=120,required = False)
    google_json_key_location = forms.CharField(max_length=120,required = False) 


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