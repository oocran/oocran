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

from neutronclient.v2_0 import client
from drivers.OpenStack.APIs.keystone.keystone import get_session


def get_public_network(vim):
    session = get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.decrypt(),
        ip=vim.ip)

    neutron = client.Client(session=session)
    networks = neutron.list_networks()
    for net in networks['networks']:
        if net['router:external'] is True:
            return net['id']