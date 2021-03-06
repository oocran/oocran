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
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from ns.models import Ns, Nvf
from scenarios.models import RRH, Scenario
from django.db import models
from .orchestrator import planification_DL, planification_UL
from time import sleep
from drivers.OpenStack.APIs.nova.nova import log


class Bbu(Nvf):
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
    radio = models.CharField(max_length=120, null=True, blank=True)
    rrh = models.ForeignKey(RRH)
    is_simulate = models.BooleanField(default=False)
    next_nvf = models.CharField(max_length=120, null=True,blank=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("bbus:details", kwargs={"id": self.id})

    def get_name(self):
        return self.name

    def get_ues(self):
        """
        Check the UE camp on the BBU
        :return:
        """
        if len(self.ues.all()) != 0:
            return self.ues
        else:
            return None

    def rb_assigment(self):
        """
        Transform BW ro rb offers
        :return:
        """
        if self.bw_dl == 1400000:
            self.rb = 18000000
        elif self.bw_dl == 3000000:
            self.rb = 36000000
        elif self.bw_dl == 5000000:
            self.rb = 72000000
        elif self.bw_dl == 10000000:
            self.rb = 150000000

    def used_frecuencys(self):
        """
        Search central frequencies assigned to the neighbourds
        :return:
        """
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
        """
        Unassign central frequency to BBU
        :return:
        """
        self.freC_DL = None
        self.freC_UL = None
        self.color_DL = "#AA0000"
        self.color_UL = "#AA0000"
        self.is_running = False
        self.save()

    def assign_frequency(self):
        """
        Assign central frequency to BBU
        :return:
        """
        self.rb_assigment()
        self.is_running = True
        frecuencies = self.used_frecuencys()
        planification_DL(self, frecuencies, self.bw_dl)
        planification_UL(self, frecuencies, self.bw_dl)

    class Meta:
        ordering = ["-timestamp", "-update"]



