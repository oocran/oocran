"""
    Open Orchestrator Cloud Radio Access Network

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from operators.models import Operator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from oocran.settings import MEDIA_ROOT
import os


def content_file_name(instance, filename):
    return '/'.join(['scripts', instance.operator.name, filename])


class Script(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=content_file_name, null=True, blank=True)
    type = models.CharField(max_length=50)
    script = models.TextField(null=True, blank=True)
    visibility = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("scripts:details", kwargs={"id": self.id})

    def check_file(self):
        if bool(self.file) is True:
            return True
        else:
            return False

    def path(self):
        return '/'.join(self.file.path.split('/')[:-1])

    def filename(self):
        return self.file.path

    def create(self, request):
        if self.type == "file":
            file = 'wget http://' + get_current_site(request).domain + '/resources/scripts/' + request.user.username + '/' + str(self.file) + '\n'
            self.script = file + self.script

        self.operator = get_object_or_404(Operator, name=request.user.username)

        if request.user.is_staff:
            self.visibility = "Public"
        else:
            self.visibility = "Private"

    class Meta:
        ordering = ["-timestamp", "-update"]
