from django.contrib import admin
from .models import BBU


class BBUModelAdmin(admin.ModelAdmin):
    list_display = ["name", "update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]
    list_editable = ["name"]
    search_fields = ["name"]

    class Meta:
        model = BBU


admin.site.register(BBU, BBUModelAdmin)