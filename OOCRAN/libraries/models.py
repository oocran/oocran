from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from operators.models import Operator


class Library(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, default="volk")
    description = models.TextField(null=True, blank=True, default="open source library")
    file = models.FileField(upload_to='nfs', null=True, blank=True)
    type = models.CharField(null=True, blank=True, max_length=50)
    script = models.TextField(default="sudo apt-get install volk")
    visibility = models.CharField(default="Private", max_length=50)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("libraries:details", kwargs={"id": self.id})

    def check_file(self):
        if bool(self.file) is False:
            return True
        else:
            return False

    class Meta:
        ordering = ["-timestamp", "-update"]
