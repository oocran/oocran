from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from ns.ns.models import Ns
from operators.models import Operator
from vnfs.models import Vnf
from scenarios.models import RRH, Scenario
from django.db import models
from .orchestrator import read_yaml, price
from .orchestrator import planification_DL, planification_UL


class Utran(Ns):
    rb_offer = models.IntegerField(default=0)
    scenario = models.ForeignKey(Scenario, null=True, blank=True)

    def get_absolut_url(self):
        return reverse("bbus:detail_utran", kwargs={"id": self.id})

    def remove_frecuencies(self):
        nvfs = BBU.objects.filter(nvfi=self).filter(operator=self.operator)
        for nvf in nvfs:
            lista = nvf.rrh.freCs.split('/')
            lista.remove(str(nvf.freC_DL - nvf.bw_dl / 2) + "-" + str(nvf.freC_DL + nvf.bw_dl / 2))
            lista.remove(str(nvf.freC_UL - nvf.bw_ul / 2) + "-" + str(nvf.freC_UL + nvf.bw_ul / 2))
            nvf.rrh.freCs = '/'.join(lista)
            nvf.delete_frec()
            nvf.rrh.save()

    def create_BBU(self, list):
        for element in list:
            bbu = BBU(**element)
            bbu.ns = self
            self.rb_offer += bbu.bw_dl
            bbu.radio = 20
            self.price += price(bbu, bbu.bw_dl)
            bbu.save()

    def create(self):
        list = read_yaml(self.file, self.operator)
        if list and list is not True and list is not False:
            self.save()
            self.create_BBU(list)
            self.save()
        if list is False:
            return False
        if list is True:
            return None
        return True


class BBU(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    ns = models.ForeignKey(Ns, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    # Downlink
    freC_DL = models.PositiveIntegerField(null=True, blank=True)
    color_DL = models.CharField(max_length=20, null=True, blank=True, default="#AA0000")
    bw_dl = models.IntegerField(null=True, blank=True)
    rb = models.IntegerField(null=True, blank=True)
    pt = models.FloatField(null=True, blank=True)
    # Uplink
    freC_UL = models.PositiveIntegerField(null=True, blank=True)
    color_UL = models.CharField(max_length=20, null=True, blank=True)
    bw_ul = models.IntegerField(null=True, blank=True)
    #
    vnf = models.ForeignKey(Vnf, null=True, blank=True)
    radio = models.CharField(max_length=120, null=True, blank=True, default=0)
    rrh = models.ForeignKey(RRH, null=True, blank=True)
    users = models.IntegerField(null=True, blank=True, default=0)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name.split('-')[1]

    def get_absolut_url(self):
        return reverse("bbus:bbu", kwargs={"id": self.id})

    def get_name(self):
        return self.name.split('-')[1]

    def rb_assigment(self):
        if self.bw_dl == 1400000:
            self.rb = 18000000
        elif self.bw_dl == 3000000:
            self.rb = 36000000
        elif self.bw_dl == 5000000:
            self.rb = 72000000
        elif self.bw_dl == 10000000:
            self.rb = 150000000

    def used_frecuencys(self):
        list = self.rrh.neighbor.strip('[').strip(']').replace("'", "").split(', ')
        neighbour = [str(x) for x in list]
        frequencies_list = []
        for rrh in neighbour:
            rrh = get_object_or_404(RRH, ip=rrh)
            frequencies = [str(x) for x in rrh.freCs.split('/')]
            for frecuency in frequencies:
                frequencies_list.append(frecuency)
        return frequencies_list

    def delete_frec(self):
        self.freC_DL = None
        self.freC_UL = None
        self.color_DL = "#AA0000"
        self.color_UL = "#AA0000"
        self.save()

    def assign_frequency(self):
        self.rb_assigment()
        frecuencies = self.used_frecuencys()
        planification_DL(self, frecuencies, self.bw_dl)
        planification_UL(self, frecuencies, self.bw_dl)

    class Meta:
        ordering = ["-timestamp", "-update"]


class Channel(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    ns = models.ForeignKey(Ns, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    sinr = models.FloatField(default=0.0)
    delay = models.FloatField(default=0.0)
    vnf = models.ForeignKey(Vnf, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


class UE(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    ns = models.ForeignKey(Ns, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    sensibility = models.FloatField(default=0.0)
    service = models.FloatField(default=3600)
    delay = models.FloatField(default=0.0)
    vnf = models.ForeignKey(Vnf, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
