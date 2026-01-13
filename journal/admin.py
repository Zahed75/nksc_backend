from django.contrib import admin
from .models import Journal

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("title", "volume", "year", "editor", "is_published")
    list_filter = ("year", "is_published")
    search_fields = ("title", "editor")
