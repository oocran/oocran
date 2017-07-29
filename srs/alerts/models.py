from __future__ import unicode_literals, absolute_import
from django.db import models
from operators.models import Operator
from ns.models import Ns, Nvf
from scenarios.models import Scenario
from django.core.urlresolvers import reverse


class Alert(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    action = models.CharField(max_length=120)
    uuid = models.UUIDField()
    ns = models.ForeignKey(Ns, null=True, blank=True)
    nvfs = models.ManyToManyField(Nvf)
    script = models.TextField(null=True, blank=True)
    scenario = models.ForeignKey(Scenario, null=True, blank=True)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("alerts:details", kwargs={"id": self.id})

    def apply_change(self):
        print "apply"

    class Meta:
        ordering = ["-timestamp", "-update"]
