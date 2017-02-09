from operators.models import Operator
from .forms import GUIForm
from vnfs.models import Vnf
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from scenarios.models import Scenario
from infrastructures.bbus.models import Utran
import json


@login_required(login_url='/login/')
def list(request):
    utrans = Utran.objects.all()

    context = {
        "user": request.user,
        "utrans": utrans,
    }

    return render(request, "epcs/list.html", context)


@login_required(login_url='/login/')
def gui(request):
    vnfs = Vnf.objects.filter(operator__name=request.user.username)
    form = GUIForm(request.POST or None)
    if form.is_valid():
        nvfi = form.save(commit=False)
        nvfi.graph = json.loads(request.POST['graph'])
        operator = get_object_or_404(Operator, name=request.user.username)
        nvfi.operator = operator
        nvfi.jsonread()
        nvfi.save()
        messages.success(request, "Deployment successfully created!", extra_tags="alert alert-success")

        return redirect("nvfis:list")

    context = {
        "user": request.user,
        "form": form,
        "object_list": vnfs,
    }
    return render(request, "gui/index.html", context)