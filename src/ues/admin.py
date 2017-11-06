from django.contrib import admin
from .models import Ue


# Register your models here.
class UeModelAdmin(admin.ModelAdmin):
    list_display = ["name", "update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]
    list_editable = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Ue


admin.site.register(Ue, UeModelAdmin)
