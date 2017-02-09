from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from operators.models import Operator


class Vnf(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, default="LTE")
    description = models.TextField(null=True, blank=True, default="SDN code for launch pyshical layer LTE TX")
    cpu = models.IntegerField(default=1)
    ram = models.IntegerField(default=1024)
    disk = models.IntegerField(default=20)
    flavor = models.CharField(max_length=120)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    interfaces = models.IntegerField(default=1)
    script = models.TextField(default="cd /home/nodea/DADES/TX_LTE/srsLTE/build/srslte/examples\n./pdsch_enodeb_file -a addr={{ip}} -l 0.3 -g {{pt}} -f {{freC}} -p {{BW}} -i ../../../rfc793.txt -m 1 >> /home/nodea/run.log")
    image = models.CharField(max_length=120, default="UBU1404SERVER6GUHD380srsLTE_AUTOSTART")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("vnfs:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-update"]

    def get_hypervisor(self):
        return self.box.split(' - ')[1]
