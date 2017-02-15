from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from operators.models import Operator
from infrastructures.bbus.forms import DeploymentForm
from .models import NVFI, Utran, BBU
from scenarios.models import Scenario
from django.contrib.auth.decorators import login_required
from OOCRAN.global_functions import paginator
import tasks


@login_required(login_url='/login/')
def create(request, id=None):
    form = DeploymentForm(request.POST or None, request.FILES or None)
    scenario = get_object_or_404(Scenario, pk=id)
    if form.is_valid():
        try:
            NVFI.objects.get(operator__name=request.user.username, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            nvfi = form.save(commit=False)
            operator = get_object_or_404(Operator, name=request.user.username)
            nvfi.operator = operator
            nvfi.scenario = scenario
            reply = nvfi.create()
            if reply is False:
                messages.success(request, "VNF is not found!", extra_tags="alert alert-danger")
            if reply is None:
                messages.success(request, "The content format is not valid!", extra_tags="alert alert-danger")
            if reply is True:
                nvfi.save()
                messages.success(request, "NVFI successfully created!", extra_tags="alert alert-success")

        return redirect("nvfis:info", id=id)

    context = {
        "user": request.user,
        "form": form,
        "scenario": scenario,
    }
    return render(request, "bbus/form.html", context)


@login_required(login_url='/login/')
def launch(request, id=None):
    utran = get_object_or_404(Utran, id=id)
    tasks.launch.delay(id)
    utran.save()

    messages.success(request, "NVFI successfully Launched!", extra_tags="alert alert-success")
    return redirect("nvfis:info", id=utran.scenario.id)


@login_required(login_url='/login/')
def shut_down(request, id=None):
    utran = get_object_or_404(Utran, id=id)
    tasks.shut_down.delay(id)

    messages.success(request, "NVFI shut down!", extra_tags="alert alert-success")
    return redirect("nvfis:info", id=utran.scenario.id)


@login_required(login_url='/login/')
def bbu(request, id=None):
    bbu = get_object_or_404(BBU, id=id)

    context = {
        "user": request.user,
        "bbu": bbu,
    }
    return render(request, "bbus/details.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    utran = get_object_or_404(Utran, pk=id)
    if utran.status == "Running":
        utran.scenario.price += round(utran.cost(), 3)
        utran.scenario.save()
        utran.shutdown()
    utran.delete()

    messages.success(request, "NVFI successfully deleted!", extra_tags="alert alert-success")
    return redirect("nvfis:info", id=utran.scenario.id)


@login_required(login_url='/login/')
def detail(request, id=None):
    utran = get_object_or_404(Utran, id=id)
    nvfs = BBU.objects.filter(nvfi__name=utran.name)
    nvfs = paginator(request, nvfs)

    context = {
        "user": utran.operator,
        "nvfi": utran,
        "object_list": nvfs,
    }
    return render(request, "nvfis/detail.html", context)