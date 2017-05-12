from django.shortcuts import render, get_object_or_404, redirect
from .models import Vnf
from images.models import Image
from operators.models import Operator, Provider
from .forms import VnfForm
from nfs.models import Nf
from django.contrib import messages
from vims.models import Vim
from drivers.Vagrant.APIs.api import list_boxes
from django.contrib.auth.decorators import login_required
from OOCRAN.global_functions import paginator
import tasks
from django.http import HttpResponse
from django.db.models import Q


@login_required(login_url='/login/')
def list(request):
    queryset_list = Vnf.objects.filter(operator__name=request.user.username)
    queryset = paginator(request, queryset_list)

    context = {
        "user": request.user,
        "object_list": queryset,
    }
    return render(request, "vnfs/list.html", context)


@login_required(login_url='/login/')
def create(request):
    nfs = Nf.objects.filter(Q(operator__name=request.user.username) | Q(operator__name="admin"))
    operator = get_object_or_404(Operator, name=request.user.username)

    if operator.vnfm == "Vagrant":
        images = list_boxes(operator)
    else:
        images = Image.objects.all()

    form = VnfForm(request.POST or None, request.FILES or None, nfs=nfs, images=images)
    if form.is_valid():
        try:
            Vnf.objects.get(operator__name=request.user.username, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            vnf = form.save(commit=False)
            vnf.operator = get_object_or_404(Operator, name=request.user.username)
            if request.user.is_staff:
                vnf.visibility = "Public"
            else:
                vnf.visibility = "Private"
            vnf.save()
            vnf.add_nf(form.cleaned_data['nf'])
            # vim = get_object_or_404(Vim, name="UPC")
            # if form.cleaned_data['create'] is True:
            # tasks.create_vnf.delay(vnf.id, vim.id)
            messages.success(request, "Successfully created!", extra_tags="alert alert-success")
        return redirect("vnfs:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("vnfs:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "vnfs/form.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    vnf = get_object_or_404(Vnf, id=id)
    # tasks.delete_vnf.delay(vnf.id)
    # image = Image.objects.get(name=vnf.name)
    # image.delete()
    vnf.delete()

    messages.success(request, "VNF successfully deleted!", extra_tags="alert alert-success")
    return redirect("vnfs:list")


@login_required(login_url='/login/')
def details(request, id=None):
    vnf = Vnf.objects.get(id=id)
        
    context = {
        "user": request.user,
        "vnf": vnf,
    }
    return render(request, "vnfs/details.html", context)


@login_required(login_url='/login/')
def state(request, id=None):
    vnf = get_object_or_404(Vnf, id=id)
    if vnf.status == "creating":
        value = False
    else:
        value = True

    return HttpResponse(value)
