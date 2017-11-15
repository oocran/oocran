from django.contrib import admin
from .models import Operator, Provider


class OperatorModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Operator

admin.site.register(Operator, OperatorModelAdmin)


class ProviderModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Provider


admin.site.register(Provider, ProviderModelAdmin)
