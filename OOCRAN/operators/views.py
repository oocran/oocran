from django.shortcuts import render, get_object_or_404, redirect
from .forms import OperatorForm, ChangeCredenForm
from .models import Operator
from django.contrib.auth.models import User
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
    user = get_object_or_404(User, username=request.user.username)
    form = ChangeCredenForm(request.POST or None, instance=user)
    if form.is_valid():
         if form.cleaned_data['password'] == form.cleaned_data['password_confirmation']:
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Password Updated!", extra_tags="alert alert-success")
            return redirect("operators:home")
         else:
            messages.success(request, "Passwords are different!", extra_tags="alert alert-danger")
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
        if form.cleaned_data['password'] == form.cleaned_data['password_confirmation']:
            operator = form.save(commit=False)
            if operator.check_used_name():
                operator.create(form.cleaned_data['email'])
                update_scenarios(operator)
                messages.success(request, "Operator successfully created!", extra_tags="alert alert-success")
                return redirect("operators:list")
            else:
                messages.success(request, "Username is already in use!", extra_tags="alert alert-danger")
        else:
            messages.success(request, "Password and confirmation are differents!", extra_tags="alert alert-danger")

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
    operator.remove()
    operator.user.delete()

    messages.success(request, "Operator successfully deleted!", extra_tags="alert alert-success")
    return redirect("operators:list")


@login_required(login_url='/login/')
def home(request):
    context = {
        "user": request.user,
    }
    return render(request, "operators/home.html", context)
