from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Image
from OOCRAN.global_functions import paginator
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from django.db.models import Q


@login_required(login_url='/login/')
def list(request):
    queryset_list = Image.objects.filter(Q(operator__name=request.user.username) | Q(operator__name="admin"))
    queryset = paginator(request, queryset_list)

    context = {
        "user": request.user,
        "images": queryset,
    }
    return render(request, "images/list.html", context)


@login_required(login_url='/login/')
def create(request):
    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            Image.objects.get(name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            image = form.save(commit=False)
            # image.download(form.cleaned_data['file'])
            image.upload()
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
def delete(request, id=None):
    image = get_object_or_404(Image, pk=id)
    image.delete()

    messages.success(request, "Image successfully deleted!", extra_tags="alert alert-success")
    return redirect("images:list")
