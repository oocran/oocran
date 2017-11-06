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
