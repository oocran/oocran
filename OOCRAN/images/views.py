from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Image
from OOCRAN.global_functions import paginator
from django.contrib.auth.decorators import login_required
from .forms import ImageForm


@login_required(login_url='/login/')
def list(request):
    queryset_list = Image.objects.filter(operator__name=request.user.username)
    queryset = paginator(request, queryset_list)

    context = {
        "user": request.user,
        "object_list": queryset,
    }
    return render(request, "nfs/libraries.html", context)


@login_required(login_url='/login/')
def image(request):
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
            return redirect("vims:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("vims:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "vims/form_images.html", context)


@login_required(login_url='/login/')
def del_img(request, id=None):
    image = get_object_or_404(Image, pk=id)
    image.delete()

    messages.success(request, "Image successfully deleted!", extra_tags="alert alert-success")
    return redirect("vims:list")
