from __future__ import absolute_import, unicode_literals
from .models import Vnf
from vims.models import Vim
from images.models import Image
from celery import task
import time
from drivers.OpenStack.deployments.vnf import create
from drivers.OpenStack.APIs.nova.nova import create_snapshot


@task()
def create_vnf(vnf, vim):
    vnf = Vnf.objects.get(pk=vnf)
    vim = Vim.objects.get(pk=vim)
    create(vnf, vim)
    time.sleep(5)
    create_snapshot(vnf)
    image = Image.objects.create(name=vnf.name, format="qcow2", operator=vnf.operator)
    print "Vnf created"


@task()
def emc():
    print "check"
