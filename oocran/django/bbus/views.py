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

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from operators.models import Operator
from .forms import AlertForm, SchedulerForm
from .models import Bbu
from ues.models import Ue
from scenarios.models import Scenario
from django.contrib.auth.decorators import login_required
from oocran.global_functions import paginator
from schedulers.models import Scheduler
import uuid
from pools.models import Channel
from alerts.models import Alert
from django.http import HttpResponse
from drivers.OpenStack.APIs.nova.nova import log


@login_required(login_url='/login/')
def details(request, id=None):
    """
    Show the BBU details
    :param request:
    :param id: BBU ID
    :return:
    """
    bbu = get_object_or_404(Bbu, id=id)
    ues = Ue.objects.filter(attached_to=bbu)
    ues = paginator(request, ues)
    alerts = Alert.objects.filter(nvfs=bbu)
    alerts = paginator(request, alerts)
    schedulers = Scheduler.objects.filter(nvfs=bbu)
    schedulers = paginator(request, schedulers)
    try:
        channel = Channel.objects.get(tx=bbu)
    except:
        channel = None

    context = {
        "user": request.user,
        "bbu": bbu,
        "ues": ues,
        "schedulers": schedulers,
        "alerts": alerts,
        "channel": channel
    }
    return render(request, "bbus/details.html", context)


@login_required(login_url='/login/')
def alert(request, id=None):
    """
    Create new alert for the BBU with id ID
    :param request:
    :param id: BBU ID
    :return:
    """
    bbu = get_object_or_404(Bbu, id=id)
    form = AlertForm(request.POST or None)
    if form.is_valid():
        try:
            Alert.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            alert = form.save(commit=False)
            alert.operator = get_object_or_404(Operator, user=request.user)
            alert.uuid = uuid.uuid4().hex
            alert.save()
            alert.nvfs.add(bbu)

            messages.success(request, "Alert created successfully!", extra_tags="alert alert-success")
        return redirect("bbus:details", id=id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("bbus:details", id=id)

    context = {
        "user": request.user,
        "bbu": bbu,
        "form": form,
    }
    return render(request, "bbus/alert.html", context)


@login_required(login_url='/login/')
def scheduler(request, id=None):
    """
    Create a new schedule for the BBU with id ID
    :param request:
    :param id: BBU ID
    :return:
    """
    bbu = get_object_or_404(Bbu, id=id)
    form = SchedulerForm(request.POST or None)
    if form.is_valid():
        try:
            Scheduler.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            scheduler = form.save(commit=False)
            scheduler.operator = get_object_or_404(Operator, user=request.user)
            scheduler.save()
            scheduler.nvfs.add(bbu)

            messages.success(request, "Scheduler created successfully!", extra_tags="alert alert-success")
        return redirect("bbus:details", id=id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("bbus:details", id=id)

    context = {
        "user": request.user,
        "bbu": bbu,
        "form": form,
    }
    return render(request, "bbus/scheduler.html", context)