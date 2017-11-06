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
    create,
    launch,
    shut_down,
    delete,
    list,
    details,
    alert,
    scheduler,
)

urlpatterns = [
    url(r'^(?P<id>\d+)/create/$', create, name='create'),
    url(r'^(?P<id>\d+)/details/$', details, name='details'),
    url(r'^(?P<id>\d+)/alert/$', alert, name='alert'),
    url(r'^(?P<id>\d+)/scheduler/$', scheduler, name='scheduler'),
    url(r'^(?P<id>\d+)/launch/$', launch, name='launch'),
    url(r'^(?P<id>\d+)/shut_down/$', shut_down, name='shut_down'),
    url(r'^(?P<id>\d+)/delete/$', delete, name='delete'),

    url(r'^$', list, name="list"),
]
