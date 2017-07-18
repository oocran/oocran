from django.conf.urls import url

from .views import (
    create,
    details,
    delete,
    list,
    listener,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/create/$', create, name='create'),
    url(r'^(?P<id>\d+)/delete/$', delete, name="delete"),
    url(r'^(?P<id>\d+)/$', details, name='details'),
    url(r'^listener/$', listener, name='listener'),
    url(r'^$', list, name="list"),
]