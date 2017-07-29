from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from operators.models import Operator
from pools.forms import PoolForm, AlertForm, SchedulerForm
from .models import Pool
from ns.models import Ns, Nvf
from bbus.models import Bbu
from scenarios.models import Scenario
from django.contrib.auth.decorators import login_required
from oocran.global_functions import paginator
from oocran import settings
from schedulers.models import Scheduler
from .tasks import celery_launch, celery_shut_down
from django.contrib.sites.shortcuts import get_current_site
import uuid
from alerts.models import Alert


@login_required(login_url='/login/')
def list(request):
    scenarios = Scenario.objects.filter(operator__user=request.user)
    scenarios = paginator(request, scenarios)

    context = {
        "user": request.user,
        "object_list": scenarios,
    }
    return render(request, "pools/list.html", context)


@login_required(login_url='/login/')
def create(request, id=None):
    scenario = get_object_or_404(Scenario, id=id)
    form = PoolForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            Ns.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            ns = form.save(commit=False)
            ns.operator = get_object_or_404(Operator, user=request.user)
            ns.scenario = scenario
            [reply, tag] = ns.create()
            messages.success(request, reply, extra_tags=tag)

        return redirect("scenarios:scenario", id=id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("scenarios:scenario", id=id)

    context = {
        "user": request.user,
        "form": form,
        "scenario": scenario,
    }
    return render(request, "pools/form.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    utran = get_object_or_404(Pool, id=id)
    id = utran.scenario.id

    try:
        utran.delete_influxdb_database()
    except:
        print "database does not exist!"

    utran.scenario.total_infras -= 1
    utran.scenario.save()

    if utran.status == "Running":
        celery_shut_down.delay(id, action="delete")
        utran.scenario.active_infras -= 1
    else:
        print "delete"

    utran.delete()

    messages.success(request, "Pool successfully deleted!", extra_tags="alert alert-success")
    return redirect("scenarios:scenario", id=id)


@login_required(login_url='/login/')
def launch(request, id=None):
    pool = get_object_or_404(Pool, id=id)
    celery_launch.delay(id)
    pool.save()

    messages.success(request, "Pool successfully Launched!", extra_tags="alert alert-success")
    return redirect("pools:details", id=pool.scenario.id)


@login_required(login_url='/login/')
def shut_down(request, id=None):
    utran = get_object_or_404(Pool, id=id)
    utran.scenario.active_infras -= 1
    utran.scenario.save()
    celery_shut_down.delay(id)

    messages.success(request, "Pool shut down!", extra_tags="alert alert-success")
    return redirect("pools:details", id=utran.scenario.id)


@login_required(login_url='/login/')
def details(request, id=None):
    pool = get_object_or_404(Pool, id=id)
    bbus = Bbu.objects.filter(ns=pool)
    schedulers = Scheduler.objects.filter(ns=pool)
    schedulers = paginator(request, schedulers)
    alerts = Alert.objects.filter(ns=pool)
    alerts = paginator(request, alerts)

    context = {
        "user": request.user,
        "utran": pool,
        "alerts": alerts,
        "bbus": bbus,
        "schedulers": schedulers,
        "url": get_current_site(request).domain.split(':')[0],
        "grafana": "http://"+settings.GRAFANA+'/?login='+pool.operator.name+'&password='+pool.operator.decrypt(),
    }
    return render(request, "pools/detail.html", context)


@login_required(login_url='/login/')
def alert(request, id=None):
    utran = get_object_or_404(Pool, id=id)
    form = AlertForm(request.POST or None, nvfs=Bbu.objects.filter(ns=utran))
    if form.is_valid():
        try:
            Alert.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            alert = form.save(commit=False)
            alert.operator = get_object_or_404(Operator, user=request.user)
            alert.scenario = utran.scenario
            alert.uuid = uuid.uuid4().hex
            alert.save()

            messages.success(request, "Alert created successfully!", extra_tags="alert alert-success")
        return redirect("pools:details")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("pools:details")

    context = {
        "user": request.user,
        "utran": utran,
        "form": form,
    }
    return render(request, "pools/alert.html", context)


@login_required(login_url='/login/')
def scheduler(request, id=None):
    utran = get_object_or_404(Pool, id=id)
    form = SchedulerForm(request.POST or None, nvfs=Bbu.objects.filter(ns=utran))
    if form.is_valid():
        try:
            Scheduler.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            scheduler = form.save(commit=False)
            scheduler.operator = get_object_or_404(Operator, user=request.user)
            scheduler.scenario = utran.scenario
            scheduler.type = "nvf"
            scheduler.ns = utran
            scheduler.save()
            for id in form.cleaned_data['nvfs']:
                scheduler.nvfs.add(get_object_or_404(Nvf, id=id))

            messages.success(request, "Scheduler created successfully!", extra_tags="alert alert-success")
        return redirect("pools:details", id=utran.id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("pools:details", id=utran.id)

    context = {
        "user": request.user,
        "utran": utran,
        "form": form,
    }
    return render(request, "pools/scheduler.html", context)