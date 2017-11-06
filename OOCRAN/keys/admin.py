from django.contrib import admin
from .models import Key


class KeyModelAdmin(admin.ModelAdmin):
    list_display = ["update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]

    class Meta:
        model = Key

admin.site.register(Key, KeyModelAdmin)