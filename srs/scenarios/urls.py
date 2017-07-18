from django.conf.urls import url

from .views import (
    create,
    details,
    delete,
    list,
    scenario,
    scenarios,
    alert,
    scheduler,
)

urlpatterns = [
    url(r'^create/$', create, name='create'),
    url(r'^(?P<id>\d+)/$', details, name='details'),
    url(r'^(?P<id>\d+)/delete/$', delete, name="delete"),
    url(r'^(?P<id>\d+)/alert/$', alert, name="alert"),
    url(r'^(?P<id>\d+)/scheduler/$', scheduler, name="scheduler"),
    url(r'^(?P<id>\d+)/scenario/$', scenario, name='scenario'),
    url(r'^scenarios/$', scenarios, name="scenarios"),
    url(r'^$', list, name="list"),
]