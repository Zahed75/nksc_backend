from django.contrib import admin
from .models import Journal
from unfold.admin import ModelAdmin





@admin.register(Journal)
class JournalAdmin(ModelAdmin):
    list_display = ("title", "volume", "year", "editor", "is_published")
    list_filter = ("year", "is_published")
    search_fields = ("title", "editor")


