from tackerclient import client
from drivers.OpenStack.APIs.keystone.keystone import get_session


def get_vnfd(vim):
    tacker = client.Client(2, session=get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.password,
        ip=vim.ip))
