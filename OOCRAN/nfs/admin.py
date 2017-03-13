from django.contrib import admin
from .models import Nf


# Register your models here.
class NfModelAdmin(admin.ModelAdmin):
    list_display = ["name", "update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]
    list_editable = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Nf


admin.site.register(Nf, NfModelAdmin)
