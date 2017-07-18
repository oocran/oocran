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
    print "NS running"


@task()
def shut_down(id, action=None):
    print "NS shut down"
