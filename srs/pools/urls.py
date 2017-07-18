from django.conf.urls import url

from .views import (
    create,
    launch,
    shut_down,
    delete,
    list,
    details,
    alert,
    scheduler,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/create/$', create, name='create'),
    url(r'^(?P<id>\d+)/details/$', details, name='details'),
    url(r'^(?P<id>\d+)/alert/$', alert, name='alert'),
    url(r'^(?P<id>\d+)/scheduler/$', scheduler, name='scheduler'),
    url(r'^(?P<id>\d+)/launch/$', launch, name='launch'),
    url(r'^(?P<id>\d+)/shut_down/$', shut_down, name='shut_down'),
    url(r'^(?P<id>\d+)/delete/$', delete, name='delete'),

    url(r'^$', list, name="list"),
]
