from django.conf.urls import url

from .views import (
    list,
    create,
    delete,
    details,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/delete/$', delete, name='delete'),
    url(r'^(?P<id>\d+)/$', details, name='details'),
    url(r'^create/$', create, name='create'),
    url(r'^$', list, name="list"),
]
