from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Vim, Device
from images.models import Image
from OOCRAN.global_functions import paginator
from django.contrib.admin.views.decorators import staff_member_required
from .forms import VimForm, DeviceForm


@staff_member_required
def list(request):
    vims = Vim.objects.all()
    vims = paginator(request, vims)

    context = {
        "user": request.user,
        "vims": vims,
    }
    return render(request, "vims/list.html", context)


@staff_member_required
def delete(request, id=None):
    vim = get_object_or_404(Vim, id=id)
    vim.delete()

    messages.success(request, "VIM successfully deleted!", extra_tags="alert alert-success")
    return redirect("vims:list")


@staff_member_required
def create(request):
    form = VimForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            Vim.objects.get(name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            if form.cleaned_data['password'] == form.cleaned_data['password_confirmation']:
                vim = form.save(commit=False)
                vim.set_public_network()
                vim.save()
                messages.success(request, "VIM successfully register!", extra_tags="alert alert-success")
            else:
                messages.success(request, "Passwords are different!", extra_tags="alert alert-danger")
            return redirect("vims:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("vims:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "vims/form.html", context)


@staff_member_required
def details(request, id=None):
    vim = get_object_or_404(Vim, id=id)

    context = {
        "user": request.user,
        "vim": vim,
    }
    return render(request, "vims/details.html", context)


###############################################################################

@staff_member_required
def device(request, id=None):
    vim = get_object_or_404(Vim, id=id)
    form = DeviceForm(request.POST or None, request.FILES or None, node=vim.get_hypervisors())
    if form.is_valid():
        try:
            Device.objects.get(name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            device = form.save(commit=False)
            device.vim = vim
            device.save()
            messages.success(request, "Device successfully registered!", extra_tags="alert alert-success")
            return redirect("vims:details", id=id)
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("vims:details", id=id)

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "vims/form_device.html", context)


@staff_member_required
def deldevice(request, id=None, pk=None):
    device = get_object_or_404(Device, id=pk)
    device.delete()

    messages.success(request, "Device successfully unregistered!", extra_tags="alert alert-success")
    return redirect("vims:details", id=id)
