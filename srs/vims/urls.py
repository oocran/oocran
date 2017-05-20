from django.conf.urls import url

from .views import (
    list,
    create,
    delete,
    details,
    device,
    deldevice,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/deldevice/(?P<pk>\d+)/$', deldevice, name='deldevice'),
    url(r'^(?P<id>\d+)/delete/$', delete, name='delete'),
    url(r'^(?P<id>\d+)/device/$', device, name='device'),
    url(r'^(?P<id>\d+)/$', details, name='details'),
    url(r'^create/$', create, name='create'),
    url(r'^$', list, name="list"),
]
