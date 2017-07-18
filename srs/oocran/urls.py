from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from operators.forms import LoginForm
from operators.views import home
from django.views.static import serve
import settings

urlpatterns = [
    url(r'^operators/', include("operators.urls", namespace='operators')),
    url(r'^vnfs/', include("vnfs.urls", namespace='vnfs')),
    url(r'^scripts/', include("scripts.urls", namespace='scripts')),
    url(r'^images/', include("images.urls", namespace='images')),
    url(r'^scenarios/', include("scenarios.urls", namespace='scenarios')),
    url(r'^ns/', include("ns.urls", namespace='ns')),
    url(r'^ues/', include("ues.urls", namespace='ues')),
    url(r'^pools/', include("pools.urls", namespace='pools')),
    url(r'^vims/', include("vims.urls", namespace='vims')),
    url(r'^schedulers/', include("schedulers.urls", namespace='schedulers')),
    url(r'^keys/', include("keys.urls", namespace='keys')),
    url(r'^alerts/', include("alerts.urls", namespace='alerts')),
    url(r'^bbus/', include("bbus.urls", namespace='bbus')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name="home"),


    url(r'^login/$', views.login, {'template_name': 'base/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name='logout'),
    url(r'^resources/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]