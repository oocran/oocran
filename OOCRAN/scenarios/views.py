from django.shortcuts import render
from .models import Scenario
from operators.models import Operator
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import ScenarioForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from OOCRAN.global_functions import paginator
from ns.ns.models import Ns


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
    rrhs = scenario.rrh.all()

    context = {
        "scenario": scenario,
        "rrhs": rrhs,
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
            scenario.save()
            reply = scenario.create_scenarios()
            if reply is False:
                messages.success(request, "The content format is not valid!", extra_tags="alert alert-danger")
            if reply is True:
                messages.success(request, "Scenario Successfully created!", extra_tags="alert alert-success")

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
