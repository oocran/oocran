from __future__ import absolute_import, unicode_literals
from .models import Utran, BBU, Channel, UE
from celery import task
from django.utils import timezone
from drivers.OpenStack.deployments.utran import create_deploy as OpenStack_create_deploy
from drivers.OpenStack.deployments.utran import delete_deploy as OpenStack_delete_deploy
from drivers.Vagrant.APIs.api import vagrant_launch as Vagrant_create_deploy
from drivers.Vagrant.APIs.api import vagrant_destroy as Vagrant_delete_deploy


@task()
def launch(id):
    utran = Utran.objects.get(id=id)
    utran.status = 'Working-launch'
    utran.save()

    bbus = BBU.objects.filter(ns=utran)
    [bbu.assign_frequency() for bbu in bbus]
    channels = Channel.objects.filter(ns=utran)
    ues = UE.objects.filter(ns=utran)

    if utran.vim_option == "Near":
        OpenStack_create_deploy(utran, bbus, channels, ues)
        [nvf.check_provision() for nvf in bbus]
        [nvf.check_provision() for nvf in channels]
        [nvf.check_provision() for nvf in ues]
    elif utran.vim_option == "Vagrant":
        Vagrant_create_deploy(utran, bbus)

    print "Provision finished"

    utran.status = 'Running'
    utran.launch_time = timezone.now()
    utran.save()
    print "NS running"


@task()
def shut_down(id, action=None):
    utran = Utran.objects.get(id=id)
    utran.status = 'Working-shutdown'
    utran.save()

    utran.scenario.price += round(utran.cost(), 3)
    utran.scenario.save()
    utran.remove_frecuencies()

    if utran.vim_option == "Near":
        OpenStack_delete_deploy(utran)
    elif utran.vim_option == "Vagrant":
        Vagrant_delete_deploy(utran)

    utran.status = 'Shut Down'
    utran.save()
    print "NS shut down"
    if action != None:
        utran.scenario.active_infras -= 1
        utran.scenario.save()
        utran.delete()

@task()
def emc():
    print "check"
