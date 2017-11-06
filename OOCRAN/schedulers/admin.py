from django.contrib import admin
from .models import Scheduler


class SchedulerModelAdmin(admin.ModelAdmin):
    list_display = ["update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]

    class Meta:
        model = Scheduler

admin.site.register(Scheduler, SchedulerModelAdmin)