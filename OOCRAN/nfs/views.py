from django.shortcuts import render, get_object_or_404, redirect
from operators.models import Operator, Provider
from .models import Nf
from libraries.models import Library
from .forms import NfForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from OOCRAN.global_functions import paginator
from django.db.models import Q


@login_required(login_url='/login/')
def list(request):
    queryset_list = Nf.objects.filter(Q(operator__name=request.user.username) | Q(operator__name="admin"))
    queryset = paginator(request, queryset_list)

    context = {
        "user": request.user,
        "object_list": queryset,
    }
    return render(request, "nfs/list.html", context)


@login_required(login_url='/login/')
def create(request):
    libraries = Library.objects.filter(Q(operator__name=request.user.username) | Q(operator__name="admin"))
    form = NfForm(request.POST or None, request.FILES or None, libraries=libraries)
    if form.is_valid():
        try:
            Nf.objects.get(operator__name=request.user.username, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            nf = form.save(commit=False)
            nf.operator = get_object_or_404(Operator, name=request.user.username)
            if request.user.is_staff:
                nf.visibility = "Public"
            nf.save()
            for library in form.cleaned_data['libraries']:
                nf.libraries.add(get_object_or_404(Library, id=library))
            messages.success(request, "Successfully created!", extra_tags="alert alert-success")

        return redirect("nfs:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("nfs:list")

    context = {
        "user": request.user,
        "form": form,
        "libraries": libraries,
    }
    return render(request, "nfs/form.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    instance = get_object_or_404(Nf, id=id)
    instance.delete()

    messages.success(request, "NF successfully deleted!", extra_tags="alert alert-success")
    return redirect("nfs:list")


@login_required(login_url='/login/')
def details(request, id=None):
    nf = Nf.objects.get(id=id)

    context = {
        "user": request.user,
        "nf": nf,
    }
    return render(request, "nfs/details.html", context)
