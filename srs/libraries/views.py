from django.contrib.sites.shortcuts import get_current_site
from .models import Library
from operators.models import Operator
from .forms import LibraryForm
from django.db.models import Q
from OOCRAN.global_functions import paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


@login_required(login_url='/login/')
def list(request):
    queryset_list = Library.objects.filter(Q(operator__name=request.user.username) | Q(operator__name="admin"))
    queryset = paginator(request, queryset_list)

    context = {
        "user": request.user,
        "libraries": queryset,
    }
    return render(request, "libraries/list.html", context)


@login_required(login_url='/login/')
def create(request):
    form = LibraryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            Library.objects.get(operator__name=request.user.username, name=form.cleaned_data['name'])
            messages.success(request, "Name repeated!", extra_tags="alert alert-danger")
        except:
            library = form.save(commit=False)
            library.create(request)
            library.operator = get_object_or_404(Operator, name=request.user.username)
            library.save()
            messages.success(request, "Library successfully added!", extra_tags="alert alert-success")
        return redirect("libraries:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("libraries:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "libraries/form.html", context)


@login_required(login_url='/login/')
def delete(request, id=None):
    library = get_object_or_404(Library, id=id)
    library.delete()

    messages.success(request, "Library successfully deleted!", extra_tags="alert alert-success")
    return redirect("libraries:list")


@login_required(login_url='/login/')
def details(request, id=None):
    library = get_object_or_404(Library, id=id)

    context = {
        "user": request.user,
        "library": library,
    }
    return render(request, "libraries/details.html", context)
