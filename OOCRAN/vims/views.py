from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import VIM
from operators.models import Provider
from OOCRAN.global_functions import paginator
from django.contrib.admin.views.decorators import staff_member_required
from .forms import VIMForm, CredentialsForm


@staff_member_required
def list(request):
    vims = VIM.objects.all()
    vims = paginator(request, vims)

    context = {
        "user": request.user,
        "object_list": vims,
    }
    return render(request, "vims/list.html", context)


@staff_member_required
def delete(request, id=None):
    vim = get_object_or_404(VIM, pk=id)
    vim.delete()

    messages.success(request, "VIM successfully deleted!", extra_tags="alert alert-success")
    return redirect("vims:list")


@staff_member_required
def create(request):
    form = VIMForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            VIM.objects.get(name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            if form.cleaned_data['password'] == form.cleaned_data['password_confirmation']:
                vim = form.save(commit=False)
                vim.save()
                messages.success(request, "VIM successfully created!", extra_tags="alert alert-success")
                return redirect("vims:list")
            else:
                messages.success(request, "Passwords are different!", extra_tags="alert alert-danger")
                return redirect("vims:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "vims/form.html", context)