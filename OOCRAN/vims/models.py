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

from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from drivers.OpenStack.APIs.neutron.neutron import get_public_network
from drivers.OpenStack.APIs.nova.nova import get_hypervisors, node_state
from Crypto.Cipher import AES
from oocran.secret_key import SECRET_KEY
import base64


class Vim(models.Model):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=120)
    ip = models.CharField(max_length=120)
    sdn_controller = models.CharField(max_length=120, null=True, blank=True)
    latitude = models.FloatField(max_length=120)
    longitude = models.FloatField(max_length=120)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("vims:details", kwargs={"id": self.id})

    def get_openstack_version(self):
        return OpenStack.objects.get(name=self.name).version


class Node(models.Model):
    ip = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    cpu = models.CharField(max_length=120)
    ram = models.CharField(max_length=120)
    disc = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    vim = models.ForeignKey(Vim, on_delete=models.CASCADE)
    priority = models.IntegerField()
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


class Device(models.Model):
    vim = models.ForeignKey(Vim, on_delete=models.CASCADE)
    node = models.CharField(max_length=15)
    name = models.CharField(max_length=120)
    vendor_id = models.CharField(max_length=4)
    product_id = models.CharField(max_length=4)
    is_assigned = models.BooleanField(default=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


class OpenStack(Vim):
    username = models.CharField(max_length=120, default="admin")
    version = models.IntegerField(default=3)
    password = models.CharField(max_length=120)
    project_domain = models.CharField(max_length=120, default="default")
    project = models.CharField(max_length=120, default="admin")
    public_network = models.CharField(max_length=120)
    domain = models.CharField(default="default", max_length=120)

    def set_public_network(self):
        self.public_network = get_public_network(self)

    def get_devices(self):
        return Device.objects.filter(vim=self)

    def get_hypervisors(self):
        return get_hypervisors(self)

    def encrypt(self, password):
        PADDING = '{'
        pad = lambda s: s + (32 - len(s) % 32) * PADDING
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        cipher = AES.new(SECRET_KEY.decode('base-64'))
        encoded = EncodeAES(cipher, password)
        return encoded

    def decrypt(self):
        PADDING = '{'
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        cipher = AES.new(SECRET_KEY.decode('base-64'))
        decoded = DecodeAES(cipher, self.password)
        return decoded

    def select_node(self, cpu, ram, disc):
        for node in get_hypervisors(self):
            if node.state == "up":
                if node.vcpus_used < node.vcpus and node.memory_mb_used < node.memory_mb and node.local_gb_used < node.local_gb:
                    if cpu <= node.vcpus - node.vcpus_used and ram <= node.memory_mb - node.memory_mb_used and disc <= node.local_gb - node.local_gb_used:
                        return node.hypervisor_hostname


class Aws(Vim):
    access_key_id = models.CharField(max_length=120)
    secret_access_key = models.CharField(max_length=120)
    session_token = models.CharField(max_length=120)
    keypair_name = models.CharField(max_length=120)

    def encrypt(self, password):
        PADDING = '{'
        pad = lambda s: s + (32 - len(s) % 32) * PADDING
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        cipher = AES.new(SECRET_KEY.decode('base-64'))
        encoded = EncodeAES(cipher, password)
        return encoded

    def decrypt(self):
        PADDING = '{'
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        cipher = AES.new(SECRET_KEY.decode('base-64'))
        decoded = DecodeAES(cipher, self.secret_access_key)
        return decoded


class Azure(Vim):
    tenant_id = models.CharField(max_length=120)
    client_id = models.CharField(max_length=120)
    client_secret = models.CharField(max_length=120)
    subscription_id = models.CharField(max_length=120)

    def encrypt(self, password):
        PADDING = '{'
        pad = lambda s: s + (32 - len(s) % 32) * PADDING
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        cipher = AES.new(SECRET_KEY.decode('base-64'))
        encoded = EncodeAES(cipher, password)
        return encoded

    def decrypt(self):
        PADDING = '{'
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        cipher = AES.new(SECRET_KEY.decode('base-64'))
        decoded = DecodeAES(cipher, self.client_secret)
        return decoded


def content_file_name(filename):
    return '/'.join(['gce', filename])


class Gce(Vim):
    google_project_id = models.CharField(max_length=120)
    google_client_email = models.CharField(max_length=120)
    google_json_key_location = models.FileField(upload_to=content_file_name, null=True, blank=True)