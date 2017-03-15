from __future__ import unicode_literals
from ns.ns.models import Ns
from django.db import models
from django.core.urlresolvers import reverse
from drivers.OpenStack.deployments.deployments import create_gui
from ns.ns.orchestrator import jsontoheat


class Epc(Ns):
    heat = models.TextField(null=True, blank=True)

    def get_absolut_url(self):
        return reverse("epcs:details", kwargs={"id": self.id})

    def jsonread(self):
        [elements, connections] = jsontoheat(self.graph)
        # create_gui(self, elements, connections)
