from __future__ import unicode_literals, absolute_import
from django.db import models
import math
from django.core.urlresolvers import reverse
from operators.models import Operator
from .orchestrator import read_yaml
from celery import task


class RRH(models.Model):
    name = models.CharField(max_length=120)
    ip = models.CharField(max_length=120)
    place = models.CharField(max_length=500)
    latitude = models.CharField(max_length=120)
    longitude = models.CharField(max_length=120)
    pt = models.IntegerField(default=20)
    neighbor = models.CharField(max_length=500, null=True, blank=True)
    bw = models.CharField(max_length=500)
    driver_version = models.CharField(max_length=20)
    freCs = models.CharField(max_length=500, null=True, blank=True, default='')
    first_band = models.CharField(max_length=50)
    second_band = models.CharField(max_length=50)
    third_band = models.CharField(max_length=50)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def start(self, band):
        if band==1400000:
            return self.first_band.split('-')[0]
        elif band==3000000:
            return self.second_band.split('-')[0]
        elif band==5000000:
            return self.third_band.split('-')[0]

    def max_dist(self, pt, f):
        f = f / 1000000  # MHz
        d = 10 ** ((pt + 107 - 20 * math.log10(f) - 32.44) / 20)
        return d

    def propagation(self, d, f, way):
        if way == 'dl':
            pmin = -107  # dBm
        elif way == 'ul':
            pmin = -123.4  # dBm

        f = f / 1000000  # MHz
        pt = pmin + 20 * math.log10(d) + 20 * math.log10(f) + 32.44
        return pt

    class Meta:
        ordering = ["-timestamp", "-update"]


class Scenario(models.Model):
    name = models.CharField(max_length=120, default="EETAC")
    latitude = models.FloatField(max_length=120, default='41.275621')
    longitude = models.FloatField(max_length=120, default='1.986591')
    description = models.TextField(default='Sample one mobile network deployed on the EETAC')
    total_infras = models.IntegerField(default=0)
    active_infras = models.IntegerField(default=0)
    ips = models.IntegerField(default=2)
    file = models.FileField(upload_to='scenarios/')
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    rrh = models.ManyToManyField(RRH)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("scenarios:details", kwargs={"id": self.id})

    def get_infrastructure(self):
        return self.total_infras

    def get_active_infrastructures(self):
        return self.active_infras

    def get_rrhs(self):
        bts = self.rrh.all()
        return bts

    def get_price(self):
        return round(self.scenario.price, 3)

    def delete_scenario(self):
        scenarios = Scenario.objects.filter(name=self.name)
        [scenario.delete() for scenario in scenarios]
        rrhs = RRH.objects.filter(place=self.name)
        [rrh.delete() for rrh in rrhs]

    def create_frontend(self, list):
        self.save()
        for rrh in list:
            rrh = RRH(**rrh)
            rrh.place = self.name
            rrh.save()
            self.rrh.add(rrh)

    def create_scenarios(self):
        list = read_yaml(self.file)
        if list:
            self.create_frontend(list)
            self.add_operator.delay(self.id)
            msn = "Scenario Successfully created!"
            tag = "alert alert-success"
            return msn, tag
        else:
            msn = "The content format is not valid!"
            tag = "alert alert-danger"
            return msn, tag

    def load_hour(self):
        deploy = self.forecast[1:].rstrip(']').split(',')[:-1]
        deploy = [int(x) for x in deploy]
        item = max(deploy, key=lambda x: x)
        array = "["
        for i in range(24):
            array += str(item) + ","
        array = array.rstrip(',')
        array += "]"
        return array

    @task()
    def add_operator(id):
        admin = Scenario.objects.get(id=id)
        operators = Operator.objects.filter()
        for operator in operators:
            if not operator.user.is_staff:
                scenario = Scenario(
                    name=admin.name,
                    latitude=admin.latitude,
                    longitude=admin.longitude,
                    description=admin.description,
                    file=admin.file,
                    operator=operator,
                    price=admin.price,
                )
                scenario.save()
                rrhs = admin.rrh.all()
                [scenario.rrh.add(rrh) for rrh in rrhs]
                scenario.save()

    def update_operators(self, operator):
        scenario = Scenario(
            name=self.name,
            latitude=self.latitude,
            longitude=self.longitude,
            description=self.description,
            file=self.file,
            operator=operator,
            price=self.price, )
        scenario.save()
        rrhs = self.rrh.all()
        [scenario.rrh.add(rrh) for rrh in rrhs]
        scenario.save()

    class Meta:
        ordering = ["-timestamp", "-update"]