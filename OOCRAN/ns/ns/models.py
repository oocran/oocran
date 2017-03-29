from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from .orchestrator import price, read_yaml, jsontoheat
from scenarios.models import Scenario
from vnfs.models import Vnf, Operator
from django.utils import timezone


class Ns(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='opnfv/')
    status = models.CharField(max_length=120, default="Shut Down")
    price = models.FloatField(default=0)
    total = models.FloatField(default=0)
    vim = models.CharField(max_length=120, default='Near')
    launch_time = models.DateTimeField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_scenario(self):
        return self.area.name

    def jsonread(self):
        [elements, connections] = jsontoheat(self.graph)
        # create_gui(self, elements, connections)

    def cost(self):
        if self.status == "Running":
            n_time = timezone.now()
            l_time = self.launch_time
            s_now = n_time.year * 31536000 + n_time.month * 86400 * 30 + n_time.day * 86400 + n_time.hour * 3600 + n_time.minute * 60 + n_time.second
            s_launch = l_time.year * 31536000 + l_time.month * 86400 * 30 + l_time.day * 86400 + l_time.hour * 3600 + l_time.minute * 60 + l_time.second
            self.total += round((self.price / 3600) * (s_now - s_launch), 3)
            self.save()
            return self.total
        else:
            return self.total

    def get_absolut_url(self):
        return reverse("ns:detail", kwargs={"id": self.id})

    def active_shutdown(self):
        return True

    class Meta:
        ordering = ["-timestamp", "-update"]
