from django.conf.urls import url


from .views import (
    home,
    add,
    list,
    delete,
    state,
)

urlpatterns = [
    url(r'^add/$', add, name="add"),
    url(r'^(?P<id>\d+)/delete/$', delete, name="delete"),
    url(r'^home/$', home, name='home'),
    url(r'^(?P<id>\d+)/state/$', state, name='state'),
    url(r'^$', list, name="list"),
]
