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

from celery import task
from .models import Key
from vims.models import Vim
from drivers.OpenStack.APIs.nova.nova import add_key, del_key


@task()
def add(id):
    for vim in Vim.objects.filter():
        key = Key.objects.filter(id=id)
        add_key(key, vim)


@task()
def delete(id):
    for vim in Vim.objects.filter():
        key = Key.objects.filter(id=id)
        del_key(key, vim)
