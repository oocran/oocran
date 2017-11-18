from django.contrib import admin
from .models import Script


# Register your models here.
class ScriptModelAdmin(admin.ModelAdmin):
    list_display = ["name", "update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]
    list_editable = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Script


admin.site.register(Script, ScriptModelAdmin)
