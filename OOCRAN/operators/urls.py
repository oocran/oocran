from django.conf.urls import url


from .views import (
    home,
    add,
    list,
    delete,
    change_password,
)

urlpatterns = [
    url(r'^change_pass/$', change_password, name="change_pass"),
    url(r'^add/$', add, name="add"),
    url(r'^(?P<id>\d+)/delete/$', delete, name="delete"),
    url(r'^home/$', home, name='home'),
    url(r'^$', list, name="list"),
]
