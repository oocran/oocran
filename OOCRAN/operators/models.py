from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from vims.models import VIM
from drivers.OpenStack.APIs.keystone.keystone import create_user, delete_user


class Operator(models.Model):
    name = models.CharField(max_length=120)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(null=True, blank=True,max_length=120)
    email = models.EmailField(null=True, blank=True)
    vnfm = models.CharField(max_length=120, default="Heat")
    vagrant_hypervisor = models.CharField(max_length=120, default="libvirt")
    price = models.FloatField(default=0)

    def __unicode__(self):
        return self.name

    def check_used_name(self):
        try:
            User.objects.get(username=self.name)
            return False
        except User.DoesNotExist:
            return True

    def create(self, email):
        user = User.objects.create_user(username=self.name, password=self.password, email=email)
        self.user = user
        if self.vnfm == "Heat":
            vims = VIM.objects.all()
            for vim in vims:
                create_user(self, vim)
        self.save()

    def remove(self):
        vims = VIM.objects.all()
        for vim in vims:
            delete_user(self, vim)


class Provider(Operator):
    fuel = models.CharField(max_length=120, default="https://10.20.0.2:8443")
    sdn = models.CharField(max_length=120, default="https://sdn:8080")
    spectrum = models.FloatField(default=0)
    cpu = models.FloatField(default=0)
    ram = models.FloatField(default=0)
