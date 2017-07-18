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
    vnf.status = 'creating'
    vnf.save()
    vim = Vim.objects.get(id=vim)
    create(vnf, vim)
    print "template launched"
    vnf.check_provision(vim)
    print "finish provision"
    create_snapshot(vnf, vim)
    print "snapshot created"
    Image.objects.create(name=vnf.name, format="qcow2", operator=vnf.operator)
    print "Image created"
    # delete(vnf, vim)
    print "Instance deleted"
    vnf.status = 'created'
    vnf.save()
    print "Vnf created!!!"


@task()
def delete_vnf(vnf):
    vnf = Vnf.objects.get(id=vnf)
    delete_image(vnf)
    print "Vnf deleted"