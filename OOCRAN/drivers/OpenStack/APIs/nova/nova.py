from novaclient import client
from drivers.OpenStack.APIs.keystone.keystone import get_session
from vims.models import VIM


def get_flavors(vnf):
    vims = VIM.objects.all()
    for vim in vims:
        nova = client.Client(2, session=get_session(vim))
        try:
            flavor = nova.flavors.find(vcpus=vnf.cpu, ram=vnf.ram, disk=vnf.disk)
        except:
            flavor = nova.flavors.create(name=vnf.name, ram=vnf.ram, vcpus=vnf.cpu, disk=vnf.disk, flavorid='auto', ephemeral=0, swap=0, rxtx_factor=1.0, is_public=True)

        flavor = flavor.name

    return flavor