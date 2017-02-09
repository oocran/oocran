from django.contrib import admin

from .models import VIM


class VIMModelAdmin(admin.ModelAdmin):
    list_display = ["name", "update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]
    list_editable = ["name"]
    search_fields = ["name"]

    class Meta:
        model = VIM


admin.site.register(VIM, VIMModelAdmin)
