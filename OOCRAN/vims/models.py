from __future__ import unicode_literals
from drivers.OpenStack.APIs.glance.glance import upload_image
from django.db import models
import os
import os.path
import urllib


class Vim(models.Model):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=120, default='OpenStack')
    ip = models.CharField(max_length=120)
    latitude = models.FloatField(max_length=120)
    longitude = models.FloatField(max_length=120)
    username = models.CharField(max_length=120, default="admin")
    password = models.CharField(max_length=120, null=True, blank=True)
    project_domain = models.CharField(max_length=120, default="default")
    project = models.CharField(max_length=120, default="admin")
    domain = models.CharField(default="default", max_length=120)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=120)
    format = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, )
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def download(self, url):
        destination = "/tmp/images"
        if os.path.exists(destination) is False:
            os.mkdir(destination)
        # You can also use the convenience method urlretrieve if you're using urllib anyway
        urllib.urlretrieve(url, os.path.join(destination, self.name + ".img"))

    def upload(self):
        upload_image(self)
