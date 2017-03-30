from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from operators.models import Operator


class Nf(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, default="srsLTE")
    description = models.TextField(null=True, blank=True, default="srsLTE Downlink")
    file = models.FileField(upload_to='nfs', null=True, blank=True)
    script = models.TextField(default="start.sh")
    dependencies = models.TextField(default="install...", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("nfs:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-update"]
