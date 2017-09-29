from __future__ import unicode_literals
from django.contrib.auth.models import User
from oocran.settings import INFLUXDB
from django.db import models
from vims.models import Vim, OpenStack
from drivers.OpenStack.APIs.keystone.keystone import create_user, delete_user
from drivers.OpenStack.deployments.operator import create_operator
from influxdb import InfluxDBClient
from drivers import Grafana
from Crypto.Cipher import AES
from oocran.secret_key import SECRET_KEY
from celery import task
import base64, os, shutil


class Operator(models.Model):
    name = models.CharField(max_length=120)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=120)
    email = models.EmailField()
    price = models.FloatField(default=0)
    state = models.CharField(max_length=50, default="Created")

    def __unicode__(self):
        return self.name

    def check_used_name(self):
        try:
            User.objects.get(username=self.name)
            return False
        except User.DoesNotExist:
            return True

    def encrypt(self):
        PADDING = '{'
        pad = lambda s: s + (32 - len(s) % 32) * PADDING
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        cipher = AES.new(SECRET_KEY.decode('base-64'))
        encoded = EncodeAES(cipher, self.password)
        return encoded

    def decrypt(self):
        PADDING = '{'
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        cipher = AES.new(SECRET_KEY.decode('base-64'))
        decoded = DecodeAES(cipher, self.password)
        return decoded

    @task()
    def add_to_vims(name):
        operator = Operator.objects.get(name=name)
        vims = OpenStack.objects.all()
        for vim in vims:
            create_user(operator, vim)
            create_operator(operator, vim)
        operator.state = "Created"
        operator.save()

    def create(self, email):
        self.state = "Creating"
        self.user = User.objects.create_user(username=self.name, password=self.password, email=email)
        self.password = self.encrypt()
        self.save()
        self.add_to_vims.delay(name=self.name)

        if not os.path.isdir(os.getcwd() + '/drivers/Vagrant/repository/'):
            os.mkdir(os.getcwd() + '/drivers/Vagrant/repository/')

        os.mkdir(os.getcwd() + '/drivers/Vagrant/repository/' + self.name)
        #self.monitoring()

    def remove(self):
        vims = OpenStack.objects.all()
        for vim in vims:
            delete_user(self, vim)
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

    def monitoring(self):
        admin = Operator.objects.filter(user__is_staff=True)[0]
        Grafana.apis.create_user(admin=admin, operator=self)
        Grafana.apis.create_organization(operator=self)
        Grafana.apis.alert_notification(operator=self)


class Provider(Operator):
    spectrum = models.FloatField(default=0)
    network = models.FloatField(default=0)
    cpu = models.FloatField(default=0)
    ram = models.FloatField(default=0)