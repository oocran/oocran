from __future__ import absolute_import, unicode_literals
from .models import Vnf
from vims.models import Vim
from images.models import Image
from celery import task
from drivers.OpenStack.deployments.vnf import create, delete
from drivers.OpenStack.APIs.nova.nova import create_snapshot
from drivers.OpenStack.APIs.glance.glance import delete_image


@task()
def create_vnf(vnf, vim):
    vnf = Vnf.objects.get(id=vnf)
    vim = Vim.objects.get(id=vim)
    create(vnf, vim)
    # create_snapshot(vnf)
    # Image.objects.create(name=vnf.name, format="qcow2", operator=vnf.operator)
    delete(vnf, vim)
    print "Vnf created!!!"


@task()
def delete_vnf(vnf):
    vnf = Vnf.objects.get(id=vnf)
    delete_image(vnf)
    print "Vnf deleted"


@task()
def emc():
    print "check"
