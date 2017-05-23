from django.conf.urls import url


from .views import (
    home,
    add,
    list,
    delete,
)

urlpatterns = [
    url(r'^add/$', add, name="add"),
    url(r'^(?P<id>\d+)/delete/$', delete, name="delete"),
    url(r'^home/$', home, name='home'),
    url(r'^$', list, name="list"),
]
