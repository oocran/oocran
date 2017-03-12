from __future__ import unicode_literals, absolute_import
from django.db import models
import math
from django.core.urlresolvers import reverse
from drivers.OpenStack.deployments.areas import create_area, delete_area
from vims.models import VIM
from operators.models import Operator
from .orchestrator import read_yaml, distance
from celery import task


class RRH(models.Model):
    name = models.CharField(max_length=120)
    ip = models.CharField(max_length=120)
    place = models.CharField(default="", max_length=500)
    latitude = models.CharField(max_length=120)
    longitude = models.CharField(max_length=120)
    pt = models.IntegerField(default=20)
    neighbor = models.CharField(max_length=500, null=True, blank=True)
    bw = models.CharField(max_length=500, default=20)
    freCs = models.CharField(max_length=500, null=True, blank=True, default='')
    first_band = models.CharField(default="2390000000-2400000000", max_length=50)
    second_band = models.CharField(default="2400000000-2500000000", max_length=50)
    third_band = models.CharField(default="2500000000-2600000000", max_length=50)
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
    infrastructures = models.CharField(max_length=120, default='0/0')
    file = models.FileField(upload_to='btss/')
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    status = models.BooleanField(default="False")
    rrh = models.ManyToManyField(RRH)
    vim = models.ForeignKey(VIM, null=True, blank=True,)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("scenarios:details", kwargs={"id": self.id})

    def get_infrastructure(self):
        return self.infrastructures.split('/')[0]

    def get_active_infrastructures(self):
        return self.infrastructures.split('/')[1]

    def get_bts(self):
        bts = self.bts.all()
        return bts

    def get_price(self):
        return round(self.scenario.price, 3)

    def delete_scenario(self):
        scenarios = Scenario.objects.filter(name=self.name)
        [scenario.delete() for scenario in scenarios]
        rrhs = RRH.objects.filter(place=self.name)
        [rrh.delete() for rrh in rrhs]

    def change_status(self, nvfi):
        if self.status is False:
            create_area(self)
            self.status = True
            self.save()
        elif self.status is True:
            self.status = False
            delete_area(self)
            self.save()
        else:
            if any(nvfi) is False:
                self.status = False
                delete_area(self)
                self.save()

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
            self.choose_vim()
            self.create_frontend(list)
            self.add_operator.delay(self.id)
        else:
            return False
        return True

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

    def choose_vim(self):
        vims = VIM.objects.all()
        res = {}
        for vim in vims:
            res[distance(self.longitude, self.latitude, vim.longitude, vim.latitude)] = vim
        res = sorted(res.items(), key=lambda x: x[0])
        self.vim = res[0][1]
        self.save()

    @task()
    def add_operator(id):
        admin = Scenario.objects.get(pk=id)
        operators = Operator.objects.filter()
        for operator in operators:
            if not operator.user.is_staff:
                scenario = Scenario(name=admin.name,
                                    latitude=admin.latitude,
                                    longitude=admin.longitude,
                                    description=admin.description,
                                    file=admin.file,
                                    operator=operator,
                                    price=admin.price,
                                    vim=admin.vim,)
                scenario.save()
                rrhs = admin.rrh.all()
                [scenario.rrh.add(rrh) for rrh in rrhs]
                scenario.save()

    class Meta:
        ordering = ["-timestamp", "-update"]