from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from operators.models import Operator
from libraries.models import Library
from django.shortcuts import get_object_or_404


class Nf(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='nfs', null=True, blank=True)
    script = models.TextField()
    libraries_order = models.TextField(blank=True, null=True)
    libraries = models.ManyToManyField(Library, blank=True)
    visibility = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("nfs:details", kwargs={"id": self.id})

    def get_libraries_order(self):
        lista = []
        order = self.libraries_order.split(',')
        for nf in order:
            print nf
            lista.append(get_object_or_404(Library, id=nf))
        return lista

    class Meta:
        ordering = ["-timestamp", "-update"]
