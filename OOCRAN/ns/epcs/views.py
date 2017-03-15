from operators.models import Operator
from .forms import EpcForm
from vnfs.models import Vnf
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Epc
import json
from OOCRAN.global_functions import paginator


@login_required(login_url='/login/')
def list(request):
    queryset_list = Epc.objects.all()
    queryset = paginator(request, queryset_list)

    context = {
        "user": request.user,
        "object_list": queryset,
        "utrans": queryset,
    }

    return render(request, "epcs/list.html", context)


@login_required(login_url='/login/')
def gui(request):
    vnfs = Vnf.objects.filter(operator__name=request.user.username)
    form = EpcForm(request.POST or None)
    if form.is_valid():
        ns = form.save(commit=False)
        ns.graph = json.loads(request.POST['graph'])
        operator = get_object_or_404(Operator, name=request.user.username)
        ns.operator = operator
        ns.jsonread()
        ns.save()
        messages.success(request, "Deployment successfully created!", extra_tags="alert alert-success")

        return redirect("epcs:list")

    context = {
        "user": request.user,
        "form": form,
        "object_list": vnfs,
    }
    return render(request, "gui/index.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    epc = get_object_or_404(Epc, pk=id)
    epc.delete()

    messages.success(request, "NVFI successfully deleted!", extra_tags="alert alert-success")
    return redirect("epcs:list")


@login_required(login_url='/login/')
def details(request, id=None):
    epc = get_object_or_404(Epc, id=id)

    context = {
        "user": epc.operator,
        "epc": epc,
    }
    return render(request, "epcs/details.html", context)
