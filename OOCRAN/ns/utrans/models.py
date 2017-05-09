from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from ns.ns.models import Ns, Nvf
import yaml
from scenarios.models import RRH, Scenario
from vims.models import Vim
from .orchestrator import distance
from django.db import models
from .orchestrator import read_bbus, price, read_channels, read_ues
from .orchestrator import planification_DL, planification_UL
from time import sleep
from drivers.OpenStack.APIs.nova.nova import log


class Utran(Ns):
    rb_offer = models.IntegerField(default=0)
    scenario = models.ForeignKey(Scenario, null=True, blank=True)

    def get_absolut_url(self):
        return reverse("utrans:detail_utran", kwargs={"id": self.id})

    def remove_frecuencies(self):
        nvfs = BBU.objects.filter(ns=self).filter(operator=self.operator)
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
            # bbu.flavor = get_flavors(bbu)
            bbu.ns = self
            self.rb_offer += bbu.bw_dl
            bbu.radio = 20
            self.price += price(bbu, bbu.bw_dl)
            bbu.save()

    def create_Channel(self, list):
        for element in list:
            bbu = get_object_or_404(BBU, name=element['bbu'])
            element.pop('bbu')
            channel = Channel(**element)
            channel.ns = self
            channel.operator = self.operator
            channel.save()
            bbu.canal = channel
            bbu.save()

    def create_UE(self, list):
        for element in list:
            bbu = get_object_or_404(BBU, name=element['bbu'])
            element.pop('bbu')
            ue = UE(**element)
            ue.ns = self
            ue.operator = self.operator
            ue.save()
            bbu.ues.add(ue)
            bbu.save()

    def create(self):
        self.scenario.total_infras += 1
        self.scenario.save()

        if self.operator.vnfm == "Vagrant":
            self.vim_option = "Vagrant"
        else:
            self.vim_option = "Near"
            if self.choose_vim() is False:
                return "There are not VIMS registered!", "alert alert-danger"

        doc = yaml.load(self.file)
        bbus = read_bbus(doc, self.operator)
        channels = read_channels(doc, self.operator)
        ues = read_ues(doc, self.operator)

        if type(bbus) is list and type(channels) is list and type(ues) is list:
            self.save()
            self.create_BBU(bbus)
            self.create_Channel(channels)
            self.create_UE(ues)
            self.save()
            self.create_influxdb_database()
            return "NS successfully created!", "alert alert-success"
        elif type(bbus) is list and type(ues) is list and channels is None:
            self.save()
            self.create_BBU(bbus)
            self.create_UE(ues)
            self.save()
            self.create_influxdb_database()
            return "NS successfully created!", "alert alert-success"
        elif type(bbus) is list and channels is None and ues is None:
            self.save()
            self.create_BBU(bbus)
            self.save()
            self.create_influxdb_database()
            return "NS successfully created!", "alert alert-success"
        else:
            return "The content format is not valid!", "alert alert-danger"

    def choose_vim(self):
        vims = Vim.objects.all()
        if len(vims) is 0:
            return False
        else:
            res = {}
            for vim in vims:
                res[distance(self.scenario.longitude, self.scenario.latitude, vim.longitude, vim.latitude)] = vim
            res = sorted(res.items(), key=lambda x: x[0])
            self.vim = res[0][1]
            self.save()


class Channel(Nvf):
    sinr = models.FloatField(default=0.0)
    delay = models.FloatField(default=0.0)

    def check_provision(self):
        res = False
        while res is False:
            nvf = self
            logging = log(name=nvf.name, domain=nvf.ns.vim.domain, username=nvf.vnf.operator.name, project_domain_name=nvf.ns.vim.project_domain, project_name=nvf.vnf.operator.name, password=nvf.vnf.operator.password, ip=nvf.ns.vim.ip)
            for line in logging.split("\n"):
                if "Cloud-init v." in line and "finished" in line:
                    return True
            sleep(20)


class UE(Nvf):
    sensibility = models.FloatField(default=0.0)
    service = models.FloatField(default=3600)
    delay = models.FloatField(default=0.0)
    longitude = models.FloatField(default=12.3)
    latitude = models.FloatField(default=1.3)

    def check_provision(self):
        res = False
        while res is False:
            nvf = self
            logging = log(name=nvf.name, domain=nvf.ns.vim.domain, username=nvf.vnf.operator.name, project_domain_name=nvf.ns.vim.project_domain, project_name=nvf.vnf.operator.name, password=nvf.vnf.operator.password, ip=nvf.ns.vim.ip)
            for line in logging.split("\n"):
                if "Cloud-init v." in line and "finished" in line:
                    return True
            sleep(20)


class BBU(Nvf):
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
    radio = models.CharField(max_length=120, null=True, blank=True)
    rrh = models.ForeignKey(RRH)
    canal = models.ForeignKey(Channel, null=True, blank=True)
    ues = models.ManyToManyField(UE, blank=True)

    def __unicode__(self):
        return self.name

    def check_provision(self):
        res = False
        while res is False:
            nvf = self
            logging = log(name=nvf.name, domain=nvf.ns.vim.domain, username=nvf.vnf.operator.name, project_domain_name=nvf.ns.vim.project_domain, project_name=nvf.vnf.operator.name, password=nvf.vnf.operator.password, ip=nvf.ns.vim.ip)
            for line in logging.split("\n"):
                if "Cloud-init v." in line and "finished" in line:
                    return True
            sleep(20)

    def get_absolut_url(self):
        return reverse("utrans:bbu", kwargs={"id": self.id})

    def get_name(self):
        return self.name

    def get_ues(self):
        if len(self.ues.all()) != 0:
            return self.ues
        else:
            return None

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



