from django.views.static import serve
from django.http import HttpResponse
import os


def get_template(request):
    return HttpResponse("template")
