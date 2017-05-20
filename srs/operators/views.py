from django.shortcuts import render, get_object_or_404, redirect
from .forms import OperatorForm, ChangeCredenForm
from .models import Operator
from vims.models import Vim
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from OOCRAN.global_functions import paginator
from scenarios.models import Scenario


def update_scenarios(operator):
    scenarios = Scenario.objects.filter(operator__user__is_staff=True)
    for scenario in scenarios:
        scenario.update_operators(operator)


@login_required(login_url='/login/')
def change_password(request):
    operator = get_object_or_404(Operator, user__username=request.user.username)
    form = ChangeCredenForm(request.POST or None, instance=operator.user)
    if form.is_valid():
         if form.cleaned_data['password'] == form.cleaned_data['password_confirmation']:
             operator.user.username = form.cleaned_data['username']
             operator.user.set_password(form.cleaned_data['password'])
             operator.user.save()
             operator.name = form.cleaned_data['username']
             operator.password = form.cleaned_data['password']
             operator.save()
             messages.success(request, "Password Updated!", extra_tags="alert alert-success")
             return redirect("operators:home")
         else:
            messages.success(request, "Passwords are different!", extra_tags="alert alert-danger")
            return redirect("operators:home")
    if form.errors:
        messages.success(request, form.errors, extra_tags="alert alert-danger")
        return redirect("operators:home")

    context = {
        "user": request.user,
        "form": form,
    }
    return render(request, "operators/change_pass.html", context)


@staff_member_required
def add(request):
    form = OperatorForm(request.POST or None)
    if form.is_valid():
        if form.cleaned_data['vnfm'] == "Heat" and len(Vim.objects.all()) == 0:
            messages.success(request, "There are not Vims register yet!!", extra_tags="alert alert-danger")
            return redirect("operators:list")
        if form.cleaned_data['password'] == form.cleaned_data['password_confirmation']:
            operator = form.save(commit=False)
            if operator.check_used_name():
                operator.create(form.cleaned_data['email'])
                update_scenarios(operator)
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
