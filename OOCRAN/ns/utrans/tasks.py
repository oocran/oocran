from __future__ import absolute_import, unicode_literals
from .models import Utran, BBU, Channel, UE
from celery import task
from django.utils import timezone
from drivers.OpenStack.deployments.deployments import create_deploy as OpenStack_create_deploy
from drivers.OpenStack.deployments.deployments import delete_deploy as OpenStack_delete_deploy
from drivers.Vagrant.APIs.api import vagrant_launch as Vagrant_create_deploy
from drivers.Vagrant.APIs.api import vagrant_destroy as Vagrant_delete_deploy


@task()
def launch(id):
    utran = Utran.objects.get(pk=id)
    utran.status = 'Launching'
    utran.save()

    bbus = BBU.objects.filter(ns__name=utran.name)
    channels = Channel.objects.filter(ns__name=utran.name)
    ues = UE.objects.filter(ns__name=utran.name)

    [bbu.assign_frequency() for bbu in bbus]

    if utran.vim_option == "Near":
        OpenStack_create_deploy(utran, bbus, channels, ues)
    elif utran.vim == "Vagrant":
        Vagrant_create_deploy(utran, bbus)

    utran.status = 'Running'
    utran.launch_time = timezone.now()
    utran.save()
    print "NS running"


@task()
def shut_down(id):
    utran = Utran.objects.get(pk=id)
    utran.status = 'Stoping'
    utran.save()

    utran.scenario.price += round(utran.cost(), 3)
    utran.scenario.save()
    utran.remove_frecuencies()

    if utran.vim == "Near":
        OpenStack_delete_deploy(utran)
    elif utran.vim == "Vagrant":
        Vagrant_delete_deploy(utran)

    utran.status = 'Shut Down'
    utran.save()
    print "NS shut down"


@task()
def emc():
    print "check"
