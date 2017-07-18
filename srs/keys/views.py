from django.shortcuts import render
from .models import Key
from operators.models import Operator
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import KeyForm
import tasks
from django.contrib.auth.decorators import login_required
from oocran.global_functions import paginator


@login_required(login_url='/login/')
def list(request):
    keys = Key.objects.filter(operator__user=request.user)
    keys = paginator(request, keys)

    context = {
        "user": request.user,
        "keys": keys,
    }
    return render(request, "keys/list.html", context)


@login_required(login_url='/login/')
def details(request, id=None):
    key = get_object_or_404(Key, id=id)

    context = {
        "user": request.user,
        "key": key,
    }
    return render(request, "keys/details.html", context)


@login_required(login_url='/login/')
def create(request, id=None):
    form = KeyForm(request.POST or None)
    if form.is_valid():
        try:
            Key.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            key = form.save(commit=False)
            key.operator = get_object_or_404(Operator, user=request.user)
            key.save()
            #tasks.add.delay(key.id)
            messages.success(request, "Key created successfully!", extra_tags="alert alert-success")
        return redirect("keys:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("keys:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "keys/form.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    key = get_object_or_404(Key, id=id)
    #tasks.delete.delay(key.id)
    key.delete()

    messages.success(request, "Key successfully deleted!", extra_tags="alert alert-success")
    return redirect("keys:list")
