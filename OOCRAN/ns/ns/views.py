from django.http import HttpResponse


def get_template(request):
    return HttpResponse("template")
