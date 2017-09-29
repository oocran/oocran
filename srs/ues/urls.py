from django.conf.urls import url
from .views import (
    create,
    delete,
    alldeletes,
    details,
    attach_to,
)

urlpatterns = [
    url(r'^$', list, name="list"),
    url(r'^(?P<id>\d+)/create/$', create, name='create'),
    url(r'^(?P<id>\d+)/attach_to/$', attach_to, name='attach_to'),
    url(r'^(?P<id>\d+)/delete/$', delete, name='delete'),
    url(r'^(?P<id>\d+)/alldeletes/$', alldeletes, name='alldeletes'),
    url(r'^(?P<id>\d+)/details/$', details, name='details'),
]
