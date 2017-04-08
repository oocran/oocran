from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.db import models
from operators.models import Operator
from nfs.models import Nf


class Vnf(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    nf = models.ManyToManyField(Nf, blank=True)
    visibility = models.CharField(max_length=50)
    image = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("vnfs:details", kwargs={"id": self.id})

    def add_nf(self, nfs):
        for id in nfs:
            self.nf.add(get_object_or_404(Nf, id=id))

    class Meta:
        ordering = ["-timestamp", "-update"]