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
from .models import Scheduler
from operators.models import Operator
from scenarios.models import Scenario
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import SchedulerForm
from django.contrib.auth.decorators import login_required
from oocran.global_functions import paginator


@login_required(login_url='/login/')
def list(request):
    schedulers = Scheduler.objects.filter(operator__user=request.user)
    schedulers = paginator(request, schedulers)

    context = {
        "user": request.user,
        "schedulers": schedulers,
    }
    return render(request, "schedulers/list.html", context)


@login_required(login_url='/login/')
def details(request, id=None):
    scheduler = get_object_or_404(Scheduler, id=id)

    context = {
        "user": request.user,
        "scheduler": scheduler,
    }
    return render(request, "schedulers/details.html", context)


@login_required(login_url='/login/')
def create(request, id=None):
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
            messages.success(request, "Scheduler created successfully!", extra_tags="alert alert-success")
        return redirect("schedulers:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("schedulers:list")

    context = {
        "user": request.user,
        "form": form,
        "scenario": scenario
    }
    return render(request, "schedulers/form.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    scheduler = get_object_or_404(Scheduler, id=id)
    scheduler.delete()

    messages.success(request, "Scheduler successfully deleted!", extra_tags="alert alert-success")
    return redirect("schedulers:list")