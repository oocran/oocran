from django.shortcuts import render
from .models import Library
from OOCRAN.global_functions import paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


@login_required(login_url='/login/')
def list(request):
    queryset_list = Library.objects.filter(operator__name=request.user.username)
    queryset = paginator(request, queryset_list)

    context = {
        "user": request.user,
        "object_list": queryset,
    }
    return render(request, "nfs/libraries.html", context)
