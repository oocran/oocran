from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.db import models
from operators.models import Operator
from nfs.models import Nf
from time import sleep
from drivers.OpenStack.APIs.nova.nova import log
from drivers.OpenStack.APIs.nova.nova import console


class Vnf(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, null=True, blank=True)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    nf = models.ManyToManyField(Nf, blank=True)
    visibility = models.CharField(max_length=50)
    image = models.CharField(max_length=120)
    create = models.BooleanField(default=False)
    log = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def check_provision(self, vim):
        res = False
        while res is False:
            logging = log(name=self.name, domain=vim.domain, username=self.operator.name, project_domain_name=vim.project_domain, project_name=self.operator.name, password=self.operator.password, ip=vim.ip)
            for line in logging.split("\n"):
                if "Cloud-init v." in line and "finished" in line:
                    self.log = logging
                    self.save()
                    return True
            sleep(20)

    def get_absolut_url(self):
        return reverse("vnfs:details", kwargs={"id": self.id})

    def add_nf(self, nfs):
        for id in nfs:
            self.nf.add(get_object_or_404(Nf, id=id))

    def check_nf(self):
        if len(self.nf) == 0:
            return False
        else:
            return self.nf.all()

    def get_console(self, vim):
        return console(name=self.name, domain=vim.domain, username=self.operator.name, project_domain_name=vim.project_domain, project_name=self.operator.name, password=self.operator.password, ip=vim.ip)['console']['url']

    class Meta:
        ordering = ["-timestamp", "-update"]