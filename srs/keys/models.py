from __future__ import unicode_literals, absolute_import
from django.db import models
from operators.models import Operator
from django.core.urlresolvers import reverse


class Key(models.Model):
    name = models.CharField(max_length=120)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    public_key = models.TextField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("keys:details", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-update"]
