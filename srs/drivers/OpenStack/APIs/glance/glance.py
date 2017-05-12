from glanceclient import client
from drivers.OpenStack.APIs.keystone.keystone import get_session
from vims.models import Vim


def delete_image(vnf):
    vims = Vim.objects.all()
    vim = vims[0]
    glance = client.Client(2, session=get_session(
        domain=vim.domain,
        username=vnf.operator.name,
        project_domain_name=vim.project_domain,
        project_name=vnf.operator.name,
        password=vnf.operator.password,
        ip=vim.ip))

    print glance.images.list()
    # .delete("aleee")
    print "delete Image!"
