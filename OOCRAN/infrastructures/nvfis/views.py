from django.shortcuts import get_object_or_404
from django.shortcuts import render
from OOCRAN.global_functions import paginator
from .models import NVFI
from infrastructures.bbus.models import BBU
from scenarios.models import Scenario
from infrastructures.bbus.models import Utran
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required(login_url='/login/')
def list(request):
    scenarios = Scenario.objects.filter(operator__name=request.user.username)
    scenarios = paginator(request, scenarios)

    context = {
        "user": request.user,
        "object_list": scenarios,
    }
    return render(request, "nvfis/list.html", context)


@login_required(login_url='/login/')
def state(request, id=None):
    nvfi = get_object_or_404(NVFI, id=id)
    if nvfi.status == "Running" or nvfi.status == "Shut Down":
        value = 1
    else:
        value = 0

    return HttpResponse(value)


@login_required(login_url='/login/')
def info(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    utrans = Utran.objects.filter(scenario=scenario)

    context = {
        "scenario": scenario,
        "utrans": utrans,
    }
    return render(request, "nvfis/info.html", context)


@login_required(login_url='/login/')
def detail(request, id=None):
    nvfi = get_object_or_404(NVFI, id=id)
    nvfs = BBU.objects.filter(nvfi__name=nvfi.name)
    nvfs = paginator(request, nvfs)

    context = {
        "user": nvfi.operator,
        "nvfi": nvfi,
        "object_list": nvfs,
    }
    return render(request, "nvfis/detail.html", context)



