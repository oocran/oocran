from .forms import UeForm, AttachForm
from .models import Ue
from scenarios.models import Scenario
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import yaml
from bbus.models import Bbu
from pools.models import Pool
from .orchestrator import read_users


@login_required(login_url='/login/')
def create(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    form = UeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        doc = yaml.load(form.cleaned_data['file'])
        [ues, tag] = read_users(doc, scenario)
        if tag == "alert alert-success":
            for ue in ues:
                Ue.objects.create(**ue)
            messages.success(request, "UE attached!", extra_tags=tag)
        else:
            messages.success(request, ues, extra_tags=tag)

        return redirect("scenarios:scenario", id=id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("scenarios:scenario", id=id)

    context = {
        "user": request.user,
        "form": form,
        "scenario": scenario,
    }
    return render(request, "ues/form.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    ue = get_object_or_404(Ue, id=id)
    id = ue.scenario.id
    ue.delete()

    return redirect("scenarios:scenario", id=id)


@login_required(login_url='/login/')
def alldeletes(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    Ue.objects.filter(scenario=scenario).delete()

    return redirect("scenarios:scenario", id=id)


@login_required(login_url='/login/')
def details(request, id=None):
    ue = get_object_or_404(Ue, id=id)

    context = {
        "user": request.user,
        "ue": ue,
    }
    return render(request, "ues/details.html", context)


@login_required(login_url='/login/')
def attach_to(request, id=None):
    bbus = Bbu.objects.filter(operator__user=request.user)
    ue = get_object_or_404(Ue, id=id)

    form = AttachForm(request.POST or None, request.FILES or None, pools=bbus)
    if form.is_valid():
        ue.attached_to = get_object_or_404(Bbu, id=form.cleaned_data['attached_to'])
        ue.save()
        return redirect("ues:details", id=id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("ues:details", id=id)

    context = {
        "user": request.user,
        "form": form,
        "ue": ue,
    }
    return render(request, "ues/attach_to.html", context)