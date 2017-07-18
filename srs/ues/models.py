from __future__ import unicode_literals
from django.db import models
from ns.models import Nvf
from time import sleep
from bbus.models import Bbu
from scenarios.models import Scenario
from drivers.OpenStack.APIs.nova.nova import log
from django.core.urlresolvers import reverse


class Ue(Nvf):
    scenario = models.ForeignKey(Scenario)
    sensibility = models.FloatField()
    service = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    ip = models.CharField(max_length=120, null=True, blank=True)
    attached_to = models.ForeignKey(Bbu, null=True, blank=True)

    def get_absolut_url(self):
        return reverse("ues:details", kwargs={"id": self.id})

    def check_provision(self):
        res = False
        while res is False:
            nvf = self
            logging = log(name=nvf.name, domain=nvf.ns.vim.domain, username=nvf.vnf.operator.name, project_domain_name=nvf.ns.vim.project_domain, project_name=nvf.vnf.operator.name, password=nvf.vnf.operator.decrypt(), ip=nvf.ns.vim.ip)
            for line in logging.split("\n"):
                if "Cloud-init v." in line and "finished" in line:
                    return True
            sleep(20)