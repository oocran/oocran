from __future__ import absolute_import, unicode_literals
from .models import Bbu
from celery import task
from drivers.Vagrant.APIs.main import vagrant_launch_nvf, vagrant_destroy_nvf, vagrant_ssh


@task()
def launch_nvf(id):
    nvf = Bbu.objects.get(id=id)
    vagrant_launch_nvf(nvf)
    print "NS running"


@task()
def shut_down_nvf(id):
    nvf = Bbu.objects.get(id=id)
    vagrant_destroy_nvf(nvf)
    print "NS shut down"


@task()
def reconfigure_nvf(id, script):
    nvf = Bbu.objects.get(id=id)
    vagrant_ssh(nvf=nvf, script=script)
    print "NS shut down"
