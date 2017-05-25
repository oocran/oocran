from __future__ import unicode_literals
from django.contrib.auth.models import User
from OOCRAN.settings import INFLUXDB
from django.db import models
from vims.models import Vim
from drivers.OpenStack.APIs.keystone.keystone import create_user, delete_user
from drivers.OpenStack.deployments.operator import create_operator
from influxdb import InfluxDBClient
import os, shutil


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
        self.user = User.objects.create_user(username=self.name, password=self.password, email=email)
        self.save()
        if self.vnfm == "Heat":
            vims = Vim.objects.all()
            for vim in vims:
                create_user(self, vim)
                create_operator(self, vim)
        else:
            os.mkdir(os.getcwd() + '/drivers/Vagrant/repository/' + self.name)
        self.save()

    def remove(self):
        if self.vnfm == "Heat":
            vims = Vim.objects.all()
            for vim in vims:
                delete_user(self, vim)
        elif self.vnfm == "Vagrant":
            shutil.rmtree(os.getcwd() + '/drivers/Vagrant/repository/' + self.name)

    def create_influxdb_user(self):
        client = InfluxDBClient(**INFLUXDB['default'])
        try:
            client.create_user(self.name, self.password, admin=False)
        except:
            client.drop_user(self.name)
            client.create_user(self.name, self.password, admin=False)
        print("Create user: " + self.name)

    def delete_influxdb_user(self):
        client = InfluxDBClient(**INFLUXDB['default'])
        try:
            client.drop_user(self.name)
            print("Delete user: " + self.name)
        except:
            print("Delete user: " + self.name)


class Provider(Operator):
    spectrum = models.FloatField(default=0)
    network = models.FloatField(default=0)
    cpu = models.FloatField(default=0)
    ram = models.FloatField(default=0)