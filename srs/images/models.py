from __future__ import unicode_literals
from django.db import models
from operators.models import Operator


class Image(models.Model):
    name = models.CharField(max_length=120)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    format = models.CharField(max_length=120)
    architecture = models.CharField(max_length=120, null=True, blank=True)
    version = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name
