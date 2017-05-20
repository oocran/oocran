from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from drivers.OpenStack.APIs.neutron.neutron import get_public_network
from drivers.OpenStack.APIs.nova.nova import get_hypervisors, node_state


class Vim(models.Model):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=120)
    ip = models.CharField(max_length=120)
    latitude = models.FloatField(max_length=120)
    longitude = models.FloatField(max_length=120)
    username = models.CharField(max_length=120, default="admin")
    password = models.CharField(max_length=120, null=True, blank=True)
    project_domain = models.CharField(max_length=120, default="default")
    project = models.CharField(max_length=120, default="admin")
    public_network = models.CharField(max_length=120, default="network")
    domain = models.CharField(default="default", max_length=120)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("vims:details", kwargs={"id": self.id})

    def set_public_network(self):
        self.public_network = get_public_network(self)

    def get_devices(self):
        return Device.objects.filter(vim__name=self.name)

    def get_hypervisors(self):
        return get_hypervisors(self)

    def change_node_state(self, node):
        node_state(self, node, state)


class Device(models.Model):
    vim = models.ForeignKey(Vim, on_delete=models.CASCADE)
    node = models.CharField(max_length=15)
    name = models.CharField(max_length=120)
    vendor_id = models.CharField(max_length=4)
    product_id = models.CharField(max_length=4)
    is_assigned = models.BooleanField(default=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
