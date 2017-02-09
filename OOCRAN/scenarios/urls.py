from django.conf.urls import url

from .views import (
    create,
    details,
    delete,
    list,
)

urlpatterns = [
    url(r'^create/$', create, name='create'),
    url(r'^(?P<id>\d+)/$', details, name='details'),
    url(r'^(?P<id>\d+)/delete/$', delete, name="delete"),
    url(r'^$', list, name="list"),
]