from novaclient import client
from drivers.OpenStack.APIs.keystone.keystone import get_session
from vims.models import Vim
import uuid


def get_flavors(nvf, vim):
    nova = client.Client(2, session=get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.password,
        ip=vim.ip))
    try:
        flavor = nova.flavors.find(vcpus=nvf.cpu, ram=nvf.ram, disk=nvf.disk)
    except:
        flavor = nova.flavors.create(name=str(uuid.uuid4()), ram=nvf.ram, vcpus=nvf.cpu, disk=nvf.disk, flavorid='auto', ephemeral=0, swap=0, rxtx_factor=1.0, is_public=True)

    return flavor.name


def create_snapshot(vnf, vim):
    nova = client.Client(2, session=get_session(
        domain=vim.domain,
        username=vnf.operator.name,
        project_domain_name=vim.project_domain,
        project_name=vnf.operator.name,
        password=vnf.operator.password,
        ip=vim.ip))
    server = nova.servers.find(name=vnf.name)
    nova.servers.create_image(server, vnf.name)
    print "Snapshot created!!"


def log(name, domain, username, project_domain_name, project_name, password, ip):
    nova = client.Client(2, session=get_session(
        domain=domain,
        username=username,
        project_domain_name=project_domain_name,
        project_name=project_name,
        password=password,
        ip=ip))

    server = nova.servers.find(name=name)
    return nova.servers.get_console_output(server)


def console(nvf):
    nova = client.Client(2, session=get_session(
        domain=nvf.ns.vim.domain,
        username=nvf.vnf.operator.name,
        project_domain_name=nvf.ns.vim.project_domain,
        project_name=nvf.vnf.operator.name,
        password=nvf.vnf.operator.password,
        ip=nvf.ns.vim.ip))

    server = nova.servers.find(name=nvf.name)
    return nova.servers.get_vnc_console(server, "novnc")
