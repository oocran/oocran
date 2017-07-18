from __future__ import absolute_import, unicode_literals
from .models import Pool, Channel
from ues.models import Ue
from bbus.models import Bbu
from celery import task
from django.utils import timezone
from drivers.OpenStack.deployments.utran import create_deploy as OpenStack_create_deploy
from drivers.OpenStack.deployments.utran import delete_deploy as OpenStack_delete_deploy
from drivers.Vagrant.APIs.main import vagrant_launch as Vagrant_create_deploy
from drivers.Vagrant.APIs.main import vagrant_destroy as Vagrant_delete_deploy


@task()
def celery_launch(id):
    pool = Pool.objects.get(id=id)
    pool.scenario.active_infras += 1
    pool.scenario.save()
    pool.status = 'Working-launch'
    pool.save()

    bbus = Bbu.objects.filter(ns=pool)
    [bbu.assign_frequency() for bbu in bbus]
    channels = Channel.objects.filter(ns=pool)
    ues = Ue.objects.filter(ns=pool)

    Vagrant_create_deploy(ns=pool, bbus=bbus, channels=channels, ues=ues)

    print "Provision finished"

    pool.status = 'Running'
    pool.launch_time = timezone.now()
    pool.save()
    print "NS running"


@task()
def celery_shut_down(id, action=None):
    pool = Pool.objects.get(id=id)
    pool.status = 'Working-shutdown'
    pool.save()

    pool.scenario.price += round(pool.cost(), 3)
    pool.scenario.save()
    pool.remove_frecuencies()

    Vagrant_delete_deploy(pool)

    pool.status = 'Shut Down'
    pool.save()
    print "NS shut down"
    if action != None:
        pool.scenario.active_infras -= 1
        pool.scenario.save()
        pool.delete()

########################################################


from schedulers.models import Scheduler
import datetime
from drivers.OpenStack.APIs.nova.nova import launch, shut_down
from drivers.Vagrant.APIs.main import vagrant_ssh, vagrant_destroy_nvf, vagrant_launch_nvf

@task()
def ns():
    schedulers = Scheduler.objects.filter(type="ns")
    for scheduler in schedulers:
        if str(scheduler.time) == datetime.datetime.now().strftime('%H:%M:00'):
            if scheduler.action == "Launch":
                scheduler.scenario.active_infras += 1
                scheduler.scenario.save()
                celery_launch.delay(id=scheduler.ns.id)
                scheduler.ns.save()
                print scheduler.name + " launched!"
            elif scheduler.action == "Shut Down":
                scheduler.scenario.active_infras -= 1
                scheduler.scenario.save()
                celery_shut_down.delay(id=scheduler.ns.id)
                scheduler.ns.save()
                print scheduler.name + " shut down!"
            if scheduler.destroy is True:
                scheduler.delete()


@task()
def nvf():
    schedulers = Scheduler.objects.filter(type="nvf")
    for scheduler in schedulers:
        if str(scheduler.time) == datetime.datetime.now().strftime('%H:%M:00'):
            if scheduler.action == "Launch":
                for nvf in scheduler.nvfs.all():
                    if scheduler.operator.vnfm == "Vagrant":
                        vagrant_launch_nvf(nvf=nvf)
                    elif scheduler.operator.vnfm == "OpenStack":
                        launch(name=nvf.name,
                               domain=nvf.ns.vim.domain,
                               username=nvf.operator.name,
                               project_domain_name=nvf.ns.vim.project_domain_name,
                               project_name=nvf.operator.name,
                               password=nvf.operator.password,
                               ip=nvf.ns.vim.ip)
            elif scheduler.action == "Shut Down":
                for nvf in scheduler.nvfs.all():
                    if scheduler.operator.vnfm == "Vagrant":
                        vagrant_destroy_nvf(nvf=nvf)
                    elif scheduler.operator.vnfm == "OpenStack":
                        shut_down(uuid=nvf.uuid,
                                  domain=nvf.ns.vim.domain,
                                  username=nvf.operator.name,
                                  project_domain_name=nvf.ns.vim.project_domain_name,
                                  project_name=nvf.operator.name,
                                  password=nvf.operator.password,
                                  ip=nvf.ns.vim.ip)
            elif scheduler.action == "Reconfigure":
                for nvf in scheduler.nvfs.all():
                    if scheduler.operator.vnfm == "Vagrant":
                        vagrant_ssh(script=scheduler.script, nvf=nvf)
            if scheduler.destroy is True:
                scheduler.delete()
