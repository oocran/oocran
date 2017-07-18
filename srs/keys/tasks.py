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
