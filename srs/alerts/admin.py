from django.contrib import admin
from .models import Alert


class AlertModelAdmin(admin.ModelAdmin):
    list_display = ["update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]

    class Meta:
        model = Alert

admin.site.register(Alert, AlertModelAdmin)