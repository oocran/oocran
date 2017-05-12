from django.contrib import admin
from .models import Vim


class VimModelAdmin(admin.ModelAdmin):
    list_display = ["name", "update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]
    list_editable = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Vim


admin.site.register(Vim, VimModelAdmin)
