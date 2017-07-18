from django.shortcuts import render, get_object_or_404, redirect
from .forms import OperatorForm, ChangeCredenForm
from .models import Operator
from vims.models import Vim
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from oocran.global_functions import paginator
from scenarios.models import Scenario
from django.http import HttpResponse


def update_scenarios(id):
    operator = Operator.objects.get(id=id)
    scenarios = Scenario.objects.filter(operator__user__is_staff=True)
    for scenario in scenarios:
        scenario.update_operators(operator)


@staff_member_required
def add(request):
    form = OperatorForm(request.POST or None)
    if form.is_valid():
        if form.cleaned_data['password'] == form.cleaned_data['password_confirmation']:
            operator = form.save(commit=False)
            if operator.check_used_name():
                operator.create(form.cleaned_data['email'])
                update_scenarios(id=operator.id)
                operator.create_influxdb_user()
                messages.success(request, "Operator successfully created!", extra_tags="alert alert-success")
                return redirect("operators:list")
            else:
                messages.success(request, "Username is already in use!", extra_tags="alert alert-danger")
        else:
            messages.success(request, "Password and confirmation are differents!", extra_tags="alert alert-danger")
        return redirect("operators:list")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("operators:list")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "operators/form.html", context)


@staff_member_required
def list(request):
    operators = Operator.objects.filter().exclude(user__is_staff=True)
    operators = paginator(request, operators)

    context = {
        "user": request.user,
        "object_list": operators,
    }
    return render(request, "operators/list.html", context)


@staff_member_required
def delete(request, id=None):
    operator = get_object_or_404(Operator, id=id)
    operator.delete_influxdb_user()
    operator.remove()
    operator.user.delete()

    messages.success(request, "Operator successfully deleted!", extra_tags="alert alert-success")
    return redirect("operators:list")


@login_required(login_url='/login/')
def home(request):
    operator = get_object_or_404(Operator, name=request.user.username)

    context = {
        "user": request.user,
        "operator": operator,
    }
    return render(request, "operators/home.html", context)


@login_required(login_url='/login/')
def state(request, id=None):
    operator = get_object_or_404(Operator, id=id)
    
    return HttpResponse(operator.state)