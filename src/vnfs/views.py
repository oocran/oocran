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

from django.shortcuts import render, get_object_or_404, redirect
from .models import Vnf
from keys.models import Key
from images.models import Image
from operators.models import Operator, Provider
from .forms import VnfForm
from scripts.models import Script
from django.contrib import messages
from drivers.Vagrant.APIs.main import list_boxes
from django.contrib.auth.decorators import login_required
from oocran.global_functions import paginator
from django.http import HttpResponse
from django.db.models import Q


@login_required(login_url='/login/')
def list(request):
    queryset_list = Vnf.objects.filter(operator__user=request.user)
    queryset = paginator(request, queryset_list)

    context = {
        "user": request.user,
        "object_list": queryset,
    }
    return render(request, "vnfs/list.html", context)


@login_required(login_url='/login/')
def create(request):
    scripts = Script.objects.filter(Q(operator__user=request.user) | Q(operator__name="admin"))
    key = Key.objects.filter(operator__user=request.user)
    images = Image.objects.all()

    form = VnfForm(request.POST or None, request.FILES or None, scripts=scripts, images=images, key=key)
    if form.is_valid():
        try:
            Vnf.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            vnf = form.save(commit=False)
            vnf.operator = get_object_or_404(Operator, user=request.user)
            if form.cleaned_data['image'] == '':
                messages.success(request, 'Image not selected!', extra_tags="alert alert-danger")
                return redirect("vnfs:list")
            if request.user.is_staff:
                vnf.visibility = "Public"
            else:
                vnf.visibility = "Private"
            vnf.save()
            for id in form.cleaned_data['scripts']:
                vnf.scripts.add(get_object_or_404(Script, id=id))
            messages.success(request, "Successfully created!", extra_tags="alert alert-success")
        return redirect("vnfs:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("vnfs:list")

    context = {
        "user": request.user,
        "form": form,
        "scripts": scripts,
    }
    return render(request, "vnfs/form.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    vnf = get_object_or_404(Vnf, id=id)
    # tasks.delete_vnf.delay(vnf.id)
    # image = Image.objects.get(name=vnf.name)
    # image.delete()
    vnf.delete()

    messages.success(request, "VNF successfully deleted!", extra_tags="alert alert-success")
    return redirect("vnfs:list")


@login_required(login_url='/login/')
def details(request, id=None):
    vnf = Vnf.objects.get(id=id)
        
    context = {
        "user": request.user,
        "vnf": vnf,
    }
    return render(request, "vnfs/details.html", context)


@login_required(login_url='/login/')
def state(request, id=None):
    vnf = get_object_or_404(Vnf, id=id)
    if vnf.status == "creating":
        value = False
    else:
        value = True

    return HttpResponse(value)
