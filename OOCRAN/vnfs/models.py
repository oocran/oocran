from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.db import models
from operators.models import Operator
from nfs.models import Nf


class Vnf(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, default="LTE")
    description = models.TextField(null=True, blank=True, default="SDN code for launch pyshical layer LTE TX")
    cpu = models.IntegerField(default=1)
    ram = models.IntegerField(default=1024)
    disk = models.IntegerField(default=20)
    flavor = models.CharField(max_length=120)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    nf = models.ManyToManyField(Nf, blank=True)
    image = models.CharField(max_length=120, default="UBU1404SERVER6GUHD380srsLTE_AUTOSTART")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("vnfs:detail", kwargs={"id": self.id})

    def get_nfs(self):
        return

    def add_nf(self, nfs):
        for id in nfs:
            print id
            self.nf.add(get_object_or_404(Nf, id=id))


    class Meta:
        ordering = ["-timestamp", "-update"]

    def get_hypervisor(self):
        return self.box.split(' - ')[1]
