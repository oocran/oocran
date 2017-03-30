from heatclient.client import Client
from time import sleep
from drivers.OpenStack.APIs.keystone.keystone import get_project_id
from drivers.OpenStack.APIs.keystone.keystone import get_token


def credentials(ns, vim):
    heat = Client('1', endpoint="http://" + vim.ip + ":8004/v1/" + get_project_id(ns.operator, vim),
                  token=get_token(ns, vim))
    return heat


def create_stack(ns, template, vim):
    heat = credentials(ns, vim)
    stack = heat.stacks.create(stack_name=ns.name, template=template, parameters={})
    uid = stack['stack']['id']

    stack = heat.stacks.get(stack_id=uid).to_dict()
    while stack['stack_status'] == 'CREATE_IN_PROGRESS':
        print "Creating stack."
        stack = heat.stacks.get(stack_id=uid).to_dict()
        sleep(10)

    if stack['stack_status'] == 'CREATE_COMPLETE':
        print "Stack succesfully created."
    else:
        return "Stack fall to unknow status: {}".format(stack)


def delete_stack(ns, vim):
    heat = credentials(ns, vim)
    stack = heat.stacks.get(ns.name)
    heat.stacks.delete(stack.parameters['OS::stack_id'])