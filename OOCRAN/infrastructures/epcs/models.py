from __future__ import unicode_literals
from infrastructures.nvfis.models import NVFI
from django.db import models
from drivers.OpenStack.deployments.deployments import create_gui
from infrastructures.nvfis.orchestrator import jsontoheat


class Epc(NVFI):
    heat = models.TextField(null=True,blank=True)

    def jsonread(self):
        [elements, connections] = jsontoheat(self.graph)
        create_gui(self, elements, connections)