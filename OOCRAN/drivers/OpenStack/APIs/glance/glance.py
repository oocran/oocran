import glanceclient.v2.client as glclient
from drivers.OpenStack.APIs.keystone.keystone import get_token_images
import glanceclient


def get_images(ns, vim):
    glance = glclient.Client("http://controller:9292", token=get_token_images())
    images = glance.images.list()
    img_list = []
    for image in list(images):
        img_list.append(image['name'])

    return img_list


def upload_image(img):
    # imagefile = "/tmp/images/cirr.img"
    glance = glclient.Client("http://controller:9292", token=get_token_images())
    with open('/tmp/cirros-0.3.4-x86_64-disk.img', 'rb') as imagefile:
        glance.images.create(name="centos", is_public="True", visibility="public", disk_format="qcow2",
                             container_format="bare", data=imagefile)
