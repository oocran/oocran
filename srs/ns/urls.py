from django.conf.urls import url
from .views import (
    state,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/state/$', state, name='state'),
]
