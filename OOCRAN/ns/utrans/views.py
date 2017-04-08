from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from operators.models import Operator
from ns.utrans.forms import DeploymentForm, DeploymentVagrantForm
from .models import Ns, Utran, BBU
from vims.models import Vim
from scenarios.models import Scenario
from django.contrib.auth.decorators import login_required
from OOCRAN.global_functions import paginator
import tasks
from django.http import HttpResponse


@login_required(login_url='/login/')
def create(request, id=None):
    operator = get_object_or_404(Operator, name=request.user.username)
    if operator.vnfm == "Vagrant":
        form = DeploymentVagrantForm(request.POST or None, request.FILES or None)
    else:
        form = DeploymentForm(request.POST or None, request.FILES or None)

    scenario = get_object_or_404(Scenario, pk=id)
    if form.is_valid():
        try:
            Ns.objects.get(operator__name=request.user.username, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            ns = form.save(commit=False)
            ns.operator = operator
            ns.scenario = scenario
            if operator.vnfm == "Vagrant":
                ns.vim = "Vagrant"
            else:
                ns.vim_option = form.cleaned_data['vim_option']
                ns.vim = get_object_or_404(Vim, name="UPC")

            [reply, tag] = ns.create()
            messages.success(request, reply, extra_tags=tag)

        return redirect("utrans:info", id=id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("utrans:info", id=id)

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

    messages.success(request, "NS successfully Launched!", extra_tags="alert alert-success")
    return redirect("utrans:info", id=utran.scenario.id)


@login_required(login_url='/login/')
def shut_down(request, id=None):
    utran = get_object_or_404(Utran, id=id)
    tasks.shut_down.delay(id)

    messages.success(request, "NS shut down!", extra_tags="alert alert-success")
    return redirect("utrans:info", id=utran.scenario.id)


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

    messages.success(request, "NS successfully deleted!", extra_tags="alert alert-success")
    return redirect("utrans:info", id=utran.scenario.id)


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
    return render(request, "utrans/detail.html", context)


##############################################################################

@login_required(login_url='/login/')
def list(request):
    scenarios = Scenario.objects.filter(operator__name=request.user.username)
    scenarios = paginator(request, scenarios)

    context = {
        "user": request.user,
        "object_list": scenarios,
    }
    return render(request, "utrans/list.html", context)


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
    utrans = paginator(request, utrans)

    context = {
        "scenario": scenario,
        "utrans": utrans,
    }
    return render(request, "utrans/info.html", context)


@login_required(login_url='/login/')
def detail_utran(request, id=None):
    utran = get_object_or_404(Utran, id=id)
    bbus = BBU.objects.filter(ns__name=utran.name)
    bbus = paginator(request, bbus)

    context = {
        "user": utran.operator,
        "nvfi": utran,
        "object_list": bbus,
    }
    return render(request, "utrans/detail.html", context)
