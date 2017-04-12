from __future__ import unicode_literals
from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=120)
    format = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name
