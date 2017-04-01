from __future__ import unicode_literals
from django.db import models
from drivers.OpenStack.APIs.glance.glance import upload_image
import os
import os.path
import urllib
from vnfs.models import Vnf


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
