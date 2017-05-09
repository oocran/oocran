from django.contrib import admin
from .models import Library


# Register your models here.
class LibraryModelAdmin(admin.ModelAdmin):
    list_display = ["name", "update", "timestamp"]
    list_display_links = ["update"]
    list_filter = ["update", "timestamp"]
    list_editable = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Library


admin.site.register(Library, LibraryModelAdmin)
