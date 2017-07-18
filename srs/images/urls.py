from django.conf.urls import url

from .views import (
    list,
    create,
    sincronize,
    delete,
)

urlpatterns = [
    url(r'^$', list, name="list"),
    url(r'^create/$', create, name='create'),
    url(r'^c/$', sincronize, name='sincronize'),
    url(r'^(?P<id>\d+)/delete/$', delete, name='delete'),
]
