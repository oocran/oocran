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

from django.shortcuts import render
from .models import Scenario
from operators.models import Operator
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import ScenarioForm, AlertForm, SchedulerForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from oocran.global_functions import paginator
from ns.models import Ns
from ues.models import Ue
from alerts.models import Alert
from schedulers.models import Scheduler
from pools.models import Pool
import uuid


@staff_member_required
def list(request):
    scenarios = Scenario.objects.filter(operator__name=request.user.username)
    scenarios = paginator(request, scenarios)

    context = {
        "user": request.user,
        "object_list": scenarios,
    }
    return render(request, "scenarios/list.html", context)


@login_required(login_url='/login/')
def details(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    ues = Ue.objects.filter(scenario=scenario)

    context = {
        "scenario": scenario,
        "ues": ues,
    }
    return render(request, "scenarios/details.html", context)


@staff_member_required
def create(request):
    form = ScenarioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            Scenario.objects.get(operator__name=request.user.username, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            scenario = form.save(commit=False)
            scenario.operator = get_object_or_404(Operator, name=request.user.username)
            [msn, tag] = scenario.create_scenarios()
            messages.success(request, msn, extra_tags=tag)
        return redirect("scenarios:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("scenarios:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "scenarios/form.html", context)


@staff_member_required
def delete(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    ns_list = Ns.objects.filter(status="running")
    [ns.shutdown() for ns in ns_list]
    scenario.delete_scenario()

    messages.success(request, "Scenario successfully deleted!", extra_tags="alert alert-success")
    return redirect("scenarios:list")


@login_required(login_url='/login/')
def scenarios(request):
    scenarios = Scenario.objects.filter(operator__user=request.user)
    scenarios = paginator(request, scenarios)

    context = {
        "user": request.user,
        "object_list": scenarios,
    }
    return render(request, "scenarios/scenarios.html", context)


@login_required(login_url='/login/')
def scenario(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    pools = Pool.objects.filter(scenario=scenario)
    pools = paginator(request, pools)
    ues = Ue.objects.filter(scenario=scenario)
    #ues = paginator(request, ues)
    schedulers = Scheduler.objects.filter(scenario=scenario)
    schedulers = paginator(request, schedulers)
    alerts = Alert.objects.filter(scenario=scenario)
    alerts = paginator(request, alerts)

    context = {
        "scenario": scenario,
        "pools": pools,
        "ues": ues,
        "schedulers": schedulers,
        "alerts": alerts,
    }
    return render(request, "scenarios/scenario.html", context)


@login_required(login_url='/login/')
def alert(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    form = AlertForm(request.POST or None)
    if form.is_valid():
        try:
            Alert.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            if form.cleaned_data['ns'] is not None:
                alert = form.save(commit=False)
                alert.operator = get_object_or_404(Operator, user=request.user)
                alert.scenario = scenario
                alert.uuid = uuid.uuid4().hex
                alert.save()
                messages.success(request, "Alert created successfully!", extra_tags="alert alert-success")
            else:
                messages.success(request, "NS not selected!", extra_tags="alert alert-danger")
        return redirect("scenarios:scenario", id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("scenarios:scenario", id)

    context = {
        "user": request.user,
        "scenario": scenario,
        "form": form,
    }
    return render(request, "scenarios/alert.html", context)


@login_required(login_url='/login/')
def scheduler(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    form = SchedulerForm(request.POST or None)
    if form.is_valid():
        try:
            Scheduler.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            scheduler = form.save(commit=False)
            scheduler.operator = get_object_or_404(Operator, user=request.user)
            scheduler.scenario = scenario
            scheduler.type = "ns"
            scheduler.save()
            msn = "Scheduler created successfully!"
            tag = "alert alert-success"
            messages.success(request, msn, extra_tags=tag)
        return redirect("scenarios:scenario", id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("scenarios:scenario", id)

    context = {
        "user": request.user,
        "form": form,
        "scenario": scenario
    }
    return render(request, "scenarios/scheduler.html", context)
