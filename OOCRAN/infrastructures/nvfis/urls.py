"""trydjango19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from .views import (
    list,
    detail,
    info,
    state,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/$', detail, name='detail'),
    url(r'^(?P<id>\d+)/state/$', state, name='state'),
    url(r'^(?P<id>\d+)/info/$', info, name='info'),
    url(r'^$', list, name="list"),
]
