from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Image
from oocran.global_functions import paginator
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from operators.models import Operator
from drivers.Vagrant.APIs.main import list_boxes
from drivers.Docker.main import docker_images


@login_required(login_url='/login/')
def list(request):
    operator = Operator.objects.get(user=request.user)
    queryset_list = Image.objects.all()
    queryset = paginator(request, queryset_list)

    context = {
        "operator": operator,
        "images": queryset,
    }
    return render(request, "images/list.html", context)


@login_required(login_url='/login/')
def create(request):
    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            Image.objects.get(operator__user=request.user, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            image = form.save(commit=False)
            image.operator = get_object_or_404(Operator, name=request.user.username)
            image.save()
            messages.success(request, "Image successfully added!", extra_tags="alert alert-success")
        return redirect("images:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("images:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "images/form.html", context)


@login_required(login_url='/login/')
def sincronize(request):
    operator = Operator.objects.get(user=request.user)
    try:
        images = docker_images()
        for image in images:
            try:
                Image.objects.get(operator__user=request.user, name=image.name)
            except:
                img = Image.objects.create(name=image.name, format="Docker", operator=operator)
                img.save()
    except:
        messages.success(request, "Docker containers was not found!", extra_tags="alert alert-danger")

    try:
        images = list_boxes()
        for image in images:
            try:
                Image.objects.get(operator__user=request.user, name=image.name)
            except:
                img = Image.objects.create(name=image.name,format=image.provider, operator=operator, version=image.version)
                img.save()
    except:
        messages.success(request, "Vagrant boxes was not found!", extra_tags="alert alert-danger")

    return redirect("images:list")


@login_required(login_url='/login/')
def delete(request, id=None):
    image = get_object_or_404(Image, id=id)
    image.delete()

    messages.success(request, "Image successfully deleted!", extra_tags="alert alert-success")
    return redirect("images:list")
