from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from operators.models import Operator
from ns.utrans.forms import DeploymentForm, UEForm
from .models import Ns, Utran, BBU, UE
from scenarios.models import Scenario
from django.contrib.auth.decorators import login_required
from OOCRAN.global_functions import paginator
import tasks
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from drivers.OpenStack.APIs.nova.nova import log


@login_required(login_url='/login/')
def create(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    form = DeploymentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            Ns.objects.get(operator__name=request.user.username, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            ns = form.save(commit=False)
            ns.operator = get_object_or_404(Operator, name=request.user.username)
            ns.scenario = scenario
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
    utran.scenario.active_infras += 1
    utran.scenario.save()
    tasks.launch.delay(id)
    utran.save()

    messages.success(request, "NS successfully Launched!", extra_tags="alert alert-success")
    return redirect("utrans:info", id=utran.scenario.id)


@login_required(login_url='/login/')
def shut_down(request, id=None):
    utran = get_object_or_404(Utran, id=id)
    utran.scenario.active_infras -= 1
    utran.scenario.save()
    tasks.shut_down.delay(id)

    messages.success(request, "NS shut down!", extra_tags="alert alert-success")
    return redirect("utrans:info", id=utran.scenario.id)


@login_required(login_url='/login/')
def bbu(request, id=None):
    bbu = get_object_or_404(BBU, id=id)
    print bbu.rrh.scenario

    context = {
        "user": request.user,
        "bbu": bbu,
    }
    return render(request, "bbus/details.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    utran = get_object_or_404(Utran, id=id)
    utran.delete_influxdb_database()
    utran.scenario.total_infras -= 1
    utran.scenario.active_infras -= 1
    utran.scenario.save()

    if utran.status == "Running":
        tasks.shut_down.delay(id, action="delete")
    else:
        print "delete"

    utran.delete()

    messages.success(request, "NS successfully deleted!", extra_tags="alert alert-success")
    return redirect("utrans:info", id=utran.scenario.id)


@login_required(login_url='/login/')
def detail(request, id=None):
    utran = get_object_or_404(Utran, id=id)
    nvfs = BBU.objects.filter(ns=utran)
    nvfs = paginator(request, nvfs)

    print utran

    context = {
        "user": utran.operator,
        "utran": utran,
        "nvfs": nvfs,
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
def info(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    utrans = Utran.objects.filter(scenario=scenario)
    utrans = paginator(request, utrans)
    ues = UE.objects.filter(scenario=scenario)
    ues = paginator(request, ues)

    context = {
        "scenario": scenario,
        "utrans": utrans,
        "ues": ues,
    }
    return render(request, "utrans/info.html", context)


@login_required(login_url='/login/')
def detail_utran(request, id=None):
    utran = get_object_or_404(Utran, id=id)
    bbus = BBU.objects.filter(ns=utran)
    bbus = paginator(request, bbus)

    context = {
        "user": utran.operator,
        "utran": utran,
        "object_list": bbus,
        "url": get_current_site(request).domain.split(':')[0],
    }
    return render(request, "utrans/detail.html", context)


@login_required(login_url='/login/')
def get_log(request, id=None):
    bbu = get_object_or_404(BBU, id=id)
    return HttpResponse(log(bbu).replace('\n', '<br>'))


@login_required(login_url='/login/')
def get_console(request, id=None):
    bbu = get_object_or_404(BBU, id=id)
    return bbu.get_console

#############################################

@login_required(login_url='/login/')
def add_ue(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    form = UEForm(request.POST or None)
    if form.is_valid():
        try:
            UE.objects.get(operator__name=request.user.username, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            ue = form.save(commit=False)
            ue.scenario = scenario
            ue.operator = get_object_or_404(Operator, name=request.user.username)
            ue.save()
            #messages.success(request, reply, extra_tags=tag)

        return redirect("utrans:info", id=id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("utrans:info", id=id)

    context = {
        "user": request.user,
        "form": form,
        "scenario": scenario,
    }
    return render(request, "partials/ues/form.html", context)