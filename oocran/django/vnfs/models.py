"""
    Open Orchestrator Cloud Radio Access Network

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.db import models
from operators.models import Operator
from images.models import Image
from keys.models import Key
from time import sleep
from scripts.models import Script
from drivers.OpenStack.APIs.nova.nova import log, console


class Vnf(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    key = models.CharField(max_length=120, null=True, blank=True)
    status = models.CharField(max_length=120, null=True, blank=True)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    visibility = models.CharField(max_length=50)
    launch_script = models.TextField(null=True, blank=True)
    scripts_order = models.TextField(blank=True, null=True)
    scripts = models.ManyToManyField(Script, blank=True)
    image = models.CharField(max_length=120)
    cpu = models.IntegerField(default=1)
    ram = models.IntegerField(default=1024)
    disc = models.IntegerField(default=3)
    provider = models.CharField(max_length=120, null=True, blank=True)
    create = models.BooleanField(default=False)
    log = models.TextField(null=True, blank=True)
    real_time = models.BooleanField(default=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_key(self):
        return Key.objects.filter(name=self.key)

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

    def add_scripts(self, scripts):
        for id in scripts:
            self.scripts.add(get_object_or_404(Script, id=id))

    def get_scripts_order(self):
        lista = []

        order = self.scripts_order.split(',')
        for id in order:
            lista.append(get_object_or_404(Script, id=id))
        return lista

    def check_scripts(self):
        if len(self.scripts.all()) == 0:
            return False
        else:
            return self.scripts.all()

    def extra_spec(self):
        properties = {}
        if self.real_time is True:
            properties["hw_cpu_policy"] = "dedicated"
            properties["hcpu_cpu_thread_policy"] = "isolate"

        return properties

    def get_console(self, vim):
        return console(name=self.name,
                       domain=vim.domain,
                       username=self.operator.name,
                       project_domain_name=vim.project_domain,
                       project_name=self.operator.name,
                       password=self.operator.decrypt(),
                       ip=vim.ip)['console']['url']

    class Meta:
        ordering = ["-timestamp", "-update"]