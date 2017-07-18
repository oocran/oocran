from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from ns.models import Ns, Nvf
from ues.models import Ue
from bbus.models import Bbu
import yaml, uuid
from vims.models import Vim
from .orchestrator import distance
from django.db import models
from .orchestrator import read_bbus, price, read_channels, read_ues
from time import sleep
from drivers.OpenStack.APIs.nova.nova import log
from drivers.Grafana.apis import create_data_source


class Pool(Ns):
    rb_offer = models.IntegerField(default=0)

    def get_absolut_url(self):
        return reverse("pools:details", kwargs={"id": self.id})

    def remove_frecuencies(self):
        nvfs = Bbu.objects.filter(ns=self).filter(operator=self.operator)
        for nvf in nvfs:
            lista = nvf.rrh.freCs.split('/')
            lista.remove(str(nvf.freC_DL - nvf.bw_dl / 2) + "-" + str(nvf.freC_DL + nvf.bw_dl / 2))
            lista.remove(str(nvf.freC_UL - nvf.bw_ul / 2) + "-" + str(nvf.freC_UL + nvf.bw_ul / 2))
            nvf.rrh.freCs = '/'.join(lista)
            nvf.delete_frec()
            nvf.rrh.save()

    def create_BBU(self, list):
        for element in list:
            bbu = Bbu(**element)
            bbu.ns = self
            bbu.uuid = uuid.uuid4().hex
            bbu.typ = "bbu"
            self.rb_offer += bbu.bw_dl
            bbu.radio = 20
            self.price += price(bbu, bbu.bw_dl)
            bbu.save()

    def create_Channel(self, list):
        for element in list:
            bbu = Bbu.objects.get(name=element['bbu'], operator=self.operator)
            element.pop('bbu')
            channel = Channel(**element)
            channel.ns = self
            channel.typ = "channel"
            channel.tx = bbu
            channel.operator = self.operator
            channel.save()

    def create_UE(self, list):
        for element in list:
            bbu = Bbu.objects.get(name=element['bbu'], operator=self.operator, ns=self)
            element.pop('bbu')
            ue = Ue(**element)
            ue.ns = self
            ue.typ = "ue"
            ue.operator = self.operator
            ue.scenario = self.scenario
            ue.attached_to = bbu
            ue.save()

    def create(self):
        doc = yaml.load(self.file)
        bbus = read_bbus(doc, self.operator)
        channels = read_channels(doc, self.operator)
        ues = read_ues(doc, self.operator)

        if type(bbus) is list and type(channels) is list and type(ues) is list:
            self.save()
            self.create_BBU(bbus)
            self.create_Channel(channels)
            self.create_UE(ues)
            self.scenario.total_infras += 1
            self.scenario.save()
            self.save()
            self.create_influxdb_database()
            create_data_source(self)
            return "NS successfully created!", "alert alert-success"
        elif type(bbus) is list and type(ues) is list and channels is None:
            self.save()
            self.create_BBU(bbus)
            self.create_UE(ues)
            self.scenario.total_infras += 1
            self.scenario.save()
            self.save()
            self.create_influxdb_database()
            create_data_source(self)
            return "NS successfully created!", "alert alert-success"
        elif type(bbus) is list and channels is None and ues is None:
            self.save()
            self.create_BBU(bbus)
            self.scenario.total_infras += 1
            self.scenario.save()
            self.save()
            self.create_influxdb_database()
            create_data_source(self)
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
    tx = models.ForeignKey(Bbu, null=True, blank=True)
    next_nvf = models.CharField(max_length=120, null=True, blank=True)

    def check_provision(self):
        res = False
        while res is False:
            nvf = self
            logging = log(name=nvf.name, domain=nvf.ns.vim.domain, username=nvf.vnf.operator.name, project_domain_name=nvf.ns.vim.project_domain, project_name=nvf.vnf.operator.name, password=nvf.vnf.operator.decrypt(), ip=nvf.ns.vim.ip)
            for line in logging.split("\n"):
                if "Cloud-init v." in line and "finished" in line:
                    return True
            sleep(20)