from __future__ import unicode_literals, absolute_import
from django.db import models
from operators.models import Operator
from ns.models import Ns, Nvf
from scenarios.models import Scenario
from django.core.urlresolvers import reverse
from pools.tasks import celery_launch, celery_shut_down
from bbus.tasks import launch_nvf, shut_down_nvf, reconfigure_nvf


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

    def execute(self):
        if self.action == "Launch":
            if self.nvfs.count() is 0:
                print "launch ns"
                celery_launch.delay(id=self.ns.id)
            else:
                for nvf in self.nvfs.all():
                    print "launch bbu " + nvf.name
                    launch_nvf.delay(id=nvf.id)

        elif self.action == "Shut Down":
            if self.nvfs.count() is 0:
                print "shut down ns"
                celery_shut_down.delay(id=self.ns.id)
            else:
                for nvf in self.nvfs.all():
                    print "shut down bbu"
                    shut_down_nvf.delay(id=nvf.id)

        elif self.action == "Reconfigure":
            for nvf in self.nvfs.all():
                print "reconfigure"
                reconfigure_nvf.delay(id=nvf.id, script=self.script)

    class Meta:
        ordering = ["-timestamp", "-update"]
