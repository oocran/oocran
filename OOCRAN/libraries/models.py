from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from operators.models import Operator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404


def content_file_name(instance, filename):
    return '/'.join(['libraries', instance.operator.name, filename])


class Library(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=content_file_name, null=True, blank=True)
    type = models.CharField(max_length=50)
    script = models.TextField()
    visibility = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("libraries:details", kwargs={"id": self.id})

    def check_file(self):
        if bool(self.file) is True:
            return True
        else:
            return False

    def create(self, request):
        if self.type == "file" or self.type == "script":
            self.type = "ungrouped"
            file = 'wget http://' + get_current_site(request).domain + '/resources/libraries/' + request.user.username + '/' + str(self.file) + '\n'
            self.script = file + self.script

        self.operator = get_object_or_404(Operator, name=request.user.username)
        if request.user.is_staff:
            self.visibility = "Public"
        else:
            self.visibility = "Private"

    class Meta:
        ordering = ["-timestamp", "-update"]
