from django.http import HttpResponse
from .models import Ns, Nvf
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def get_template(request):
    return HttpResponse("template")


@login_required(login_url='/login/')
def state(request, id=None):
    ns = get_object_or_404(Ns, id=id)
    if ns.status == "Working-launch" or ns.status == "Working-shutdown":
        value = False
    else:
        value = True

    return HttpResponse(value)
