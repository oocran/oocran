from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from operators.forms import LoginForm
from operators.views import home
import settings

urlpatterns = [
    url(r'^operators/', include("operators.urls", namespace='operators')),
    url(r'^vnfs/', include("vnfs.urls", namespace='vnfs')),
    url(r'^libraries/', include("libraries.urls", namespace='libraries')),
    url(r'^images/', include("images.urls", namespace='images')),
    url(r'^nfs/', include("nfs.urls", namespace='nfs')),
    url(r'^scenarios/', include("scenarios.urls", namespace='scenarios')),
    url(r'^ns/', include("ns.ns.urls", namespace='ns')),
    url(r'^bbus/', include("ns.bbus.urls", namespace='bbus')),
    url(r'^vims/', include("vims.urls", namespace='vims')),
    url(r'^epcs/', include("ns.epcs.urls", namespace='epcs')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', home,name="home"),


    url(r'^login/$', views.login, {'template_name': 'base/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name='logout'),
    url(r'^resources/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
]