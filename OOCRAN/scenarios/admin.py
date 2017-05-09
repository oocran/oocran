from django.contrib import admin
from .models import RRH, Scenario


class RRHModelAdmin(admin.ModelAdmin):
    list_display = ["ip", "update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]
    list_editable = ["ip"]
    search_fields = ["ip"]

    class Meta:
        model = RRH

admin.site.register(RRH, RRHModelAdmin)


class ScenarioModelAdmin(admin.ModelAdmin):
    list_display = ["name", "update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]
    list_editable = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Scenario

admin.site.register(Scenario, ScenarioModelAdmin)

