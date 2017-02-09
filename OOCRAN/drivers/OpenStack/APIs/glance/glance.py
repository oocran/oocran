import glanceclient.v2.client as glclient
from drivers.OpenStack.APIs.keystone.keystone import get_token


def get_images(operator, scenario):
    glance = glclient.Client("http://"+scenario.vim.ip+":9292", token=get_token(operator, scenario))
    images = glance.images.list()
    img_list = []
    for image in list(images):
        img_list.append(image['name'])

    return img_list