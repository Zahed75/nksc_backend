from django.contrib import admin
from journal.models import *



@admin.register(JournalPage)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'volume', 'year', 'editor')
    search_fields = ('title', 'editor')
