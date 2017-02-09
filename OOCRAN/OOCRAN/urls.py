from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from operators.forms import LoginForm
from operators.views import home

urlpatterns = [
    url(r'^operators/', include("operators.urls", namespace='operators')),
    url(r'^vnfs/', include("vnfs.urls", namespace='vnfs')),
    url(r'^scenarios/', include("scenarios.urls", namespace='scenarios')),
    url(r'^nvfis/', include("infrastructures.nvfis.urls", namespace='nvfis')),
    url(r'^bbus/', include("infrastructures.bbus.urls", namespace='bbus')),
    url(r'^vims/', include("vims.urls", namespace='vims')),
    url(r'^epcs/', include("infrastructures.epcs.urls", namespace='epcs')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', home,name="home"),


    url(r'^login/$', views.login, {'template_name': 'base/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name='logout'),
]