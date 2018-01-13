"""
    Open Orchestrator Cloud Radio Access Network

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

from django.conf.urls import url

from .views import (
    details,
    alert,
    scheduler,
    #ue,
    #log,
    #console,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/details/$', details, name='details'),
    url(r'^(?P<id>\d+)/alert/$', alert, name='alert'),
    url(r'^(?P<id>\d+)/ue/$', ue, name='ue'),
    url(r'^(?P<id>\d+)/scheduler/$', scheduler, name='scheduler'),
    url(r'^(?P<id>\d+)/log/$', log, name='log'),
    url(r'^(?P<id>\d+)/console/$', console, name='console'),
    url(r'^$', list, name="list"),
]
