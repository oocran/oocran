from django.conf.urls import url

from .views import (
    list,
    create,
    delete,
    image,
    del_img,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/delete/$', delete, name='delete'),
    url(r'^(?P<id>\d+)/del_img/$', del_img, name='del_img'),
    url(r'^image/$', image, name='image'),
    url(r'^create/$', create, name='create'),
    url(r'^$', list, name="list"),
]
