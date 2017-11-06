"""
    Open Orchestrator Cloud Radio Access Network

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

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