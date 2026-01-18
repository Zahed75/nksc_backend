from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    AboutSection, TimelineEvent, Director, 
    Facility, Statistic, ContactInfo
)


class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'section_type_display', 'display_order', 'is_active')
    list_filter = ('section_type', 'is_active')
    search_fields = ('title', 'content')
    list_editable = ('display_order', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'subtitle', 'content', 'icon')
        }),
        (_('Type & Display'), {
            'fields': ('section_type', 'display_order', 'is_active')
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def section_type_display(self, obj):
        return obj.get_section_type_display()
    section_type_display.short_description = 'Section Type'


class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('year', 'title', 'description')
    list_editable = ('display_order', 'is_active')
    
    fieldsets = (
        (_('Event Details'), {
            'fields': ('year', 'title', 'description', 'icon', 'image')
        }),
        (_('Display'), {
            'fields': ('display_order', 'is_active')
        }),
    )


class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'director_type_display', 'period', 'display_order', 'is_active')  # Added display_order
    list_filter = ('director_type', 'is_active')
    search_fields = ('name', 'position', 'bio')
    list_editable = ('display_order', 'is_active')  # Fixed: display_order is now in list_display
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'position', 'director_type', 'period')
        }),
        (_('Details'), {
            'fields': ('bio', 'qualifications', 'email', 'phone', 'image')
        }),
        (_('Social Links'), {
            'fields': ('website', 'linkedin'),
            'classes': ('collapse',)
        }),
        (_('Display'), {
            'fields': ('display_order', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def director_type_display(self, obj):
        return obj.get_director_type_display()
    director_type_display.short_description = 'Type'


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'room_number', 'display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description', 'location')
    list_editable = ('display_order', 'is_active')
    
    fieldsets = (
        (_('Facility Information'), {
            'fields': ('title', 'description', 'icon', 'image')
        }),
        (_('Location Details'), {
            'fields': ('location', 'room_number', 'capacity')
        }),
        (_('Display'), {
            'fields': ('display_order', 'is_active')
        }),
    )


class StatisticAdmin(admin.ModelAdmin):
    list_display = ('label', 'value_with_format', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    
    fieldsets = (
        (_('Statistic'), {
            'fields': ('label', 'value', 'prefix', 'suffix', 'icon')
        }),
        (_('Display'), {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    def value_with_format(self, obj):
        return f"{obj.prefix}{obj.value}{obj.suffix}"
    value_with_format.short_description = 'Formatted Value'


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'contact_type_display', 'display_order', 'is_active')
    list_filter = ('contact_type', 'is_active')
    list_editable = ('display_order', 'is_active')
    
    def contact_type_display(self, obj):
        return obj.get_contact_type_display()
    contact_type_display.short_description = 'Type'


# Register all models
admin.site.register(AboutSection, AboutSectionAdmin)
admin.site.register(TimelineEvent, TimelineEventAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Statistic, StatisticAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)