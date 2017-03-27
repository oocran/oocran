from django.shortcuts import render, get_object_or_404, redirect
from operators.models import Operator, Provider
from .models import Nf
from .forms import NfForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from OOCRAN.global_functions import paginator


@login_required(login_url='/login/')
def list(request):
    queryset_list = Nf.objects.filter(operator__name=request.user.username)
    queryset = paginator(request, queryset_list)

    context = {
        "user": request.user,
        "object_list": queryset,
    }
    return render(request, "nfs/list.html", context)


@login_required(login_url='/login/')
def create(request):
    form = NfForm(request.POST or None, request.FILES or None)
    print form.errors
    if form.is_valid():
        try:
            Nf.objects.get(operator__name=request.user.username, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            nf = form.save(commit=False)
            nf.operator = get_object_or_404(Operator, name=request.user.username)
            messages.success(request, "Successfully created!", extra_tags="alert alert-success")
            nf.save()
        return redirect("nfs:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("nfs:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "nfs/form.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    instance = get_object_or_404(Nf, id=id)
    instance.delete()

    messages.success(request, "VNF successfully deleted!", extra_tags="alert alert-success")
    return redirect("nfs:list")


@login_required(login_url='/login/')
def detail(request, id=None):
    instance = Nf.objects.get(id=id)

    context = {
        "user": request.user,
        "vnf": instance,
    }
    return render(request, "nfs/detail.html", context)
