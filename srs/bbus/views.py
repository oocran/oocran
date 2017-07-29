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
    bbu = get_object_or_404(Bbu, id=id)
    form = AlertForm(request.POST or None)
    if form.is_valid():
        try:
            Alert.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            alert = form.save(commit=False)
            alert.operator = get_object_or_404(Operator, user=request.user)
            alert.nvfs = bbu
            alert.uuid = uuid.uuid4().hex
            alert.save()

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


@login_required(login_url='/login/')
def log(request, id=None):
    bbu = get_object_or_404(Bbu, id=id)
    return HttpResponse(log(bbu).replace('\n', '<br>'))


@login_required(login_url='/login/')
def console(request, id=None):
    bbu = get_object_or_404(Bbu, id=id)
    return bbu.get_console


@login_required(login_url='/login/')
def ue(request, id=None):
    print "olaa"