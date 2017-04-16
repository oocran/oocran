from __future__ import unicode_literals
from django.contrib.auth.models import User
from OOCRAN.settings import INFLUXDB
from django.db import models
from vims.models import Vim
from drivers.OpenStack.APIs.keystone.keystone import create_user, delete_user
from drivers.OpenStack.deployments.infrastructure import create_infrastructure
from influxdb import InfluxDBClient


class Operator(models.Model):
    name = models.CharField(max_length=120)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=120)
    email = models.EmailField(null=True, blank=True)
    vnfm = models.CharField(max_length=120)
    vagrant_hypervisor = models.CharField(max_length=120)
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
        self.save()
        if self.vnfm == "Heat":
            vims = Vim.objects.all()
            for vim in vims:
                create_user(self, vim)
                create_infrastructure(self, vim)
        self.save()

    def remove(self):
        if self.vnfm == "Heat":
            vims = Vim.objects.all()
            for vim in vims:
                delete_user(self, vim)

    def create_influxdb_user(self):
        dbuser = self.name
        dbuser_password = self.password
        client = InfluxDBClient(**INFLUXDB['default'])
        print("Create user: " + dbuser)
        client.create_user(dbuser, dbuser_password, admin=False)

    def delete_influxdb_user(self):
        dbuser = self.name
        client = InfluxDBClient(**INFLUXDB['default'])
        print("Delete user: " + dbuser)
        client.drop_user(dbuser)


class Provider(Operator):
    spectrum = models.FloatField(default=0)
    network = models.FloatField(default=0)
    cpu = models.FloatField(default=0)
    ram = models.FloatField(default=0)