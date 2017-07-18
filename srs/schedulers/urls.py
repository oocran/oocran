from django.conf.urls import url

from .views import (
    create,
    details,
    delete,
    list,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/create/$', create, name='create'),
    url(r'^(?P<id>\d+)/delete/$', delete, name="delete"),
    url(r'^(?P<id>\d+)/$', details, name='details'),
    url(r'^$', list, name="list"),
]