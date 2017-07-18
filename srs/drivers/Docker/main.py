import docker


class Img:
    def __init__(self, name):
        self.name = name


def docker_images():
        client = docker.from_env()
        queryset_list = []
        for tag in client.images.list():
            queryset_list.append(Img(name=tag.attrs['RepoTags'][0]))
        return queryset_list