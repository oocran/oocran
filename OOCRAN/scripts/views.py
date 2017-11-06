"""
    Open Orchestrator Cloud Radio Access Network

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

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
    print script.file

    context = {
        "user": request.user,
        "script": script,
    }
    return render(request, "scripts/details.html", context)
