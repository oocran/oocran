from django.shortcuts import get_object_or_404
from django.shortcuts import render
from OOCRAN.global_functions import paginator
from .models import Ns
from ns.bbus.models import BBU
from scenarios.models import Scenario
from ns.bbus.models import Utran
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
    return render(request, "ns/list.html", context)


@login_required(login_url='/login/')
def state(request, id=None):
    nvfi = get_object_or_404(Ns, id=id)
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
    return render(request, "ns/info.html", context)


@login_required(login_url='/login/')
def detail(request, id=None):
    ns = get_object_or_404(Ns, id=id)
    bbus = BBU.objects.filter(nvfi__name=nvfi.name)
    bbus = paginator(request, bbus)

    context = {
        "user": ns.operator,
        "nvfi": ns,
        "object_list": bbus,
    }
    return render(request, "ns/detail.html", context)
