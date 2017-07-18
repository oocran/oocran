from django.conf.urls import url

from .views import (
    details,
    alert,
    scheduler,
    ue,
    log,
    console,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/details/$', details, name='details'),
    url(r'^(?P<id>\d+)/alert/$', alert, name='alert'),
    url(r'^(?P<id>\d+)/ue/$', ue, name='ue'),
    url(r'^(?P<id>\d+)/scheduler/$', scheduler, name='scheduler'),
    url(r'^(?P<id>\d+)/log/$', log, name='log'),
    url(r'^(?P<id>\d+)/console/$', console, name='console'),
    url(r'^$', list, name="list"),
]
