from __future__ import unicode_literals, absolute_import
from django.db import models
from ns.models import Ns, Nvf
from operators.models import Operator
from scenarios.models import Scenario
from django.core.urlresolvers import reverse


def content_file_name(instance, filename):
    return '/'.join(['schedulers', instance.operator.name, filename])


class Scheduler(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=120)
    action = models.CharField(max_length=120)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, null=True, on_delete=models.CASCADE)
    ns = models.ForeignKey(Ns, null=True, on_delete=models.CASCADE)
    nvfs = models.ManyToManyField(Nvf)
    time = models.TimeField(default="12:00")
    script = models.TextField(null=True, blank=True)
    destroy = models.BooleanField(default=False)
    file = models.FileField(upload_to=content_file_name, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("schedulers:details", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-update"]