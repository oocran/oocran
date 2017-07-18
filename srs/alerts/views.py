from django.shortcuts import render
from .models import Alert
from operators.models import Operator
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import AlertForm
from django.contrib.auth.decorators import login_required
from oocran.global_functions import paginator
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from oocran import settings
import json, uuid
from bbus.models import Bbu
from pools.tasks import celery_launch, celery_shut_down


@login_required(login_url='/login/')
def list(request):
    alerts = Alert.objects.filter(operator__user=request.user)
    alerts = paginator(request, alerts)

    context = {
        "user": request.user,
        "alerts": alerts,
    }
    return render(request, "alerts/list.html", context)


@login_required(login_url='/login/')
def details(request, id=None):
    alert = get_object_or_404(Alert, id=id)

    context = {
        "user": request.user,
        "alert": alert,
    }
    return render(request, "alerts/details.html", context)


@login_required(login_url='/login/')
def create(request, id=None):
    bbu = get_object_or_404(Bbu, id=id)
    form = AlertForm(request.POST or None)
    if form.is_valid():
        try:
            Alert.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            alert = form.save(commit=False)
            alert.operator = get_object_or_404(Operator, user=request.user)
            alert.nvf = bbu
            alert.uuid = uuid.uuid4().hex
            alert.save()

            messages.success(request, "Alert created successfully!", extra_tags="alert alert-success")
        return redirect("alerts:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("alerts:list")

    context = {
        "user": request.user,
        "bbu": bbu,
        "form": form,
    }
    return render(request, "alerts/form.html", context)


@login_required(login_url='/login/')
def delete(request, id = None):
    alert = get_object_or_404(Alert, id=id)
    alert.delete()

    messages.success(request, "Alert successfully deleted!", extra_tags="alert alert-success")
    return redirect("alerts:list")


@csrf_exempt
def listener(request):
    for value in request:
        webhook = json.loads(value)
        if settings.GRAFANA in webhook['ruleUrl']:
            try:
                msn = webhook['message'].replace("{","").replace("}","")
                uuid = msn.split(',')[0].split(':')[1]
                name = msn.split(',')[1].split(':')[1]
                passw = msn.split(',')[2].split(':')[1]
            except:
                return HttpResponse('pong')

            try:
                alert = Alert.objects.get(uuid=uuid)
                if alert.operator.decrypt() == passw and alert.operator.name == name:
                    if alert.action == "Launch":
                        celery_launch.delay(id=alert.ns.id)
                    elif alert.action == "Shut Down":
                        celery_shut_down.delay(id=alert.ns.id)
                    elif alert.action == "Reconfigure":
                        print "aaaa"
            except:
                return HttpResponse('pong')

    return HttpResponse('pong')
