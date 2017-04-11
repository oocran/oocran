from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Vim
from images.models import Image
from OOCRAN.global_functions import paginator
from django.contrib.admin.views.decorators import staff_member_required
from .forms import VimForm


@staff_member_required
def list(request):
    vims = Vim.objects.all()
    images = Image.objects.all()
    vims = paginator(request, vims)
    images = paginator(request, images)

    context = {
        "user": request.user,
        "vims": vims,
        "images": images,
    }
    return render(request, "vims/list.html", context)


@staff_member_required
def delete(request, id=None):
    vim = get_object_or_404(Vim, pk=id)
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
                messages.success(request, "VIM successfully created!", extra_tags="alert alert-success")
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