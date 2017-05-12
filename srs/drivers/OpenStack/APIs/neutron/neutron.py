from neutronclient.v2_0 import client
from drivers.OpenStack.APIs.keystone.keystone import get_session


def get_public_network(vim):
    session = get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.password,
        ip=vim.ip)

    neutron = client.Client(session=session)
    networks = neutron.list_networks()
    for net in networks['networks']:
        if net['router:external'] is True:
            return net['id']
