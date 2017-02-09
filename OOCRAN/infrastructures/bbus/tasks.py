from __future__ import absolute_import, unicode_literals
from .models import Utran
from celery import task
from django.utils import timezone
import time


@task()
def launch(id):
    utran = Utran.objects.get(pk=id)
    utran.status = 'Launching'
    utran.save()
    print "execute code"
    time.sleep(30)
    utran.status = 'Running'
    utran.launch_time = timezone.now()
    utran.save()
    print "NVFI running"


@task()
def shut_down(id):
    utran = Utran.objects.get(pk=id)
    utran.status = 'Stoping'
    utran.save()
    print "execute code"
    time.sleep(30)
    utran.status = 'Shut Down'
    utran.save()
    print "NVFI shut down"


@task()
def marti():
    print "MARTIIIIIIIIIIIIIIII"

