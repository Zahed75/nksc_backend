from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Department, Staff, StaffEducation, StaffExperience


class StaffEducationInline(admin.TabularInline):
    model = StaffEducation
    extra = 1
    fields = ('degree', 'institution', 'year', 'description', 'display_order')


class StaffExperienceInline(admin.TabularInline):
    model = StaffExperience
    extra = 1
    fields = ('position', 'organization', 'start_date', 'end_date', 'is_current', 'description', 'display_order')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'staff_count', 'icon', 'display_order')
    list_display_links = ('name', 'slug')
    search_fields = ('name', 'description')
    list_editable = ('display_order',)
    readonly_fields = ('slug', 'staff_count')
    prepopulated_fields = {}
    
    def staff_count(self, obj):
        return obj.staff_count
    staff_count.short_description = 'Staff Count'


class StaffAdmin(admin.ModelAdmin):
    list_display = (
        'name_display',
        'designation_display',
        'department',
        'email',
        'phone',
        'is_active',  # Plain boolean field (editable)
        'display_order'
    )
    list_display_links = ('name_display',)
    list_filter = ('designation', 'department', 'is_active', 'join_date')
    search_fields = ('name', 'email', 'phone', 'bio', 'qualifications')
    list_editable = ('is_active', 'display_order')  # Both fields are in list_display
    readonly_fields = ('slug', 'created_at', 'updated_at', 'full_title_display')
    inlines = [StaffEducationInline, StaffExperienceInline]
    
    fieldsets = (
        (_('Personal Information'), {
            'fields': ('name', 'slug', 'designation', 'department', 'full_title_display')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'alternate_phone')
        }),
        (_('Professional Details'), {
            'fields': ('bio', 'qualifications', 'research_interests')
        }),
        (_('Media Files'), {
            'fields': ('profile_image', 'cv')
        }),
        (_('Social Links'), {
            'fields': ('website', 'linkedin', 'google_scholar', 'researchgate', 'orcid'),
            'classes': ('collapse',)
        }),
        (_('Office Details'), {
            'fields': ('office_room', 'office_hours', 'join_date')
        }),
        (_('Status & Display'), {
            'fields': ('is_active', 'display_order')
        }),
        (_('SEO Metadata'), {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def name_display(self, obj):
        return obj.name
    name_display.short_description = 'Name'
    
    def designation_display(self, obj):
        return obj.get_designation_display()
    designation_display.short_description = 'Designation'
    
    def full_title_display(self, obj):
        return obj.full_title
    full_title_display.short_description = 'Full Title'
    
    actions = ['activate_staff', 'deactivate_staff']
    
    def activate_staff(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} staff members activated.')
    activate_staff.short_description = "Activate selected staff"
    
    def deactivate_staff(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} staff members deactivated.')
    deactivate_staff.short_description = "Deactivate selected staff"


class StaffEducationAdmin(admin.ModelAdmin):
    list_display = ('staff', 'degree', 'institution', 'year', 'display_order')
    list_filter = ('staff', 'year')
    search_fields = ('degree', 'institution', 'staff__name')
    list_editable = ('display_order',)


class StaffExperienceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'position', 'organization', 'start_date', 'end_date', 'is_current')
    list_filter = ('staff', 'organization', 'is_current')
    search_fields = ('position', 'organization', 'staff__name')


# Register models
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(StaffEducation, StaffEducationAdmin)
admin.site.register(StaffExperience, StaffExperienceAdmin)