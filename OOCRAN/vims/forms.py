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


class VimForm(forms.Form):
    name = forms.CharField(max_length=32)
    type = forms.ChoiceField(required=True,widget=forms.Select(attrs={"onChange": 'select(this);'}), choices=[('OpenStack', 'OpenStack'),('AWS','AWS'),('GCE', 'GCE'), ('Azure','Azure')])
    #version = forms.ChoiceField(required=True,widget=forms.Select(attrs={"onChange": 'select(this);'}), choices=[('2', 'Mitaka'),('3','Newton')])

    ip = forms.CharField(max_length=32, initial="controller")
    #sdn_controller = forms.CharField(max_length=32,required = False)
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
    google_json_key_location = forms.FileField(required = False)