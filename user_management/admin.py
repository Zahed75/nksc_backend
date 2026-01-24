from django.contrib import admin
from .models import UserProfile
from django.utils.html import format_html
from .models import UserProfile, Chairman

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")




@admin.register(Chairman)
class ChairmanAdmin(admin.ModelAdmin):
    list_display = [
        'name_english',
        'designation_english',
        'is_active_display',
        'display_order',
        'created_at'
    ]

    list_filter = ['is_active', 'created_at']

    search_fields = [
        'name_english',
        'name_bangla',
        'designation_english',
        'designation_bangla',
        'email'
    ]

    readonly_fields = ['created_at', 'updated_at', 'profile_preview', 'signature_preview']

    list_editable = ['display_order']

    ordering = ['display_order', '-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name_bangla',
                'name_english',
                'designation_bangla',
                'designation_english',
            )
        }),

        ('Biography', {
            'fields': (
                'bio_bangla',
                'bio_english',
            ),
            'classes': ('collapse', 'open')
        }),

        ('Academic & Professional Info', {
            'fields': (
                'qualifications',
                'current_positions',
                'previous_positions',
            ),
            'classes': ('collapse',)
        }),

        ('Contact Information', {
            'fields': (
                'email',
                'phone',
            ),
            'classes': ('collapse',)
        }),

        ('Media Files', {
            'fields': (
                'profile_image',
                'profile_preview',
                'signature_image',
                'signature_preview',
            )
        }),

        ('Display Settings', {
            'fields': (
                'is_active',
                'display_order',
            )
        }),

        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )

    def is_active_display(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">● Active</span>'
            )
        return format_html(
            '<span style="color: red;">● Inactive</span>'
        )

    is_active_display.short_description = 'Status'

    def profile_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border: 1px solid #ddd; padding: 5px;" />',
                obj.profile_image.url
            )
        return "No profile image uploaded"

    profile_preview.short_description = 'Profile Preview'

    def signature_preview(self, obj):
        if obj.signature_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 100px; border: 1px solid #ddd; padding: 5px;" />',
                obj.signature_image.url
            )
        return "No signature image uploaded"

    signature_preview.short_description = 'Signature Preview'

    def save_model(self, request, obj, form, change):
        """Custom save method if needed"""
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        """Customize form if needed"""
        form = super().get_form(request, obj, **kwargs)
        return form