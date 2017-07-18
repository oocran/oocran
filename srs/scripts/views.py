from django.contrib.sites.shortcuts import get_current_site
from .models import Script
from operators.models import Operator
from .forms import ScriptForm
from django.db.models import Q
from oocran.global_functions import paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


@login_required(login_url='/login/')
def list(request):
    scripts = Script.objects.filter(Q(operator__name=request.user.username) | Q(operator__name="admin"))
    scripts = paginator(request, scripts)

    context = {
        "user": request.user,
        "scripts": scripts,
    }
    return render(request, "scripts/list.html", context)


@login_required(login_url='/login/')
def create(request):
    form = ScriptForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            Script.objects.get(operator__name=request.user.username, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            library = form.save(commit=False)
            library.create(request)
            library.operator = get_object_or_404(Operator, name=request.user.username)
            library.save()
            messages.success(request, "Script successfully added!", extra_tags="alert alert-success")
        return redirect("scripts:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("scripts:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "scripts/form.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    script = get_object_or_404(Script, id=id)
    script.delete()

    messages.success(request, "Library successfully deleted!", extra_tags="alert alert-success")
    return redirect("scripts:list")


@login_required(login_url='/login/')
def details(request, id=None):
    script = get_object_or_404(Script, id=id)

    context = {
        "user": request.user,
        "script": script,
    }
    return render(request, "scripts/details.html", context)
