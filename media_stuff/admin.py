from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django import forms
from media_stuff.models import *

# ========== SIMPLE FORMS ==========

class GalleryImageForm(forms.ModelForm):
    """Simple form for image upload"""

    class Meta:
        model = GalleryImage
        fields = ['image', 'caption', 'display_order', 'is_cover']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate image size
            if image.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError("Image size should be less than 10MB")
        return image


class GalleryVideoForm(forms.ModelForm):
    """Simple form for video upload"""

    class Meta:
        model = GalleryVideo
        fields = ['video_url', 'title', 'description', 'display_order']

    def clean_video_url(self):
        url = self.cleaned_data.get('video_url')
        if url:
            if not ('youtube.com' in url or 'youtu.be' in url or 'vimeo.com' in url):
                raise forms.ValidationError(
                    "Please enter a valid YouTube or Vimeo URL"
                )
        return url


# ========== SIMPLE INLINES ==========

class GalleryImageInline(admin.TabularInline):
    """Simple inline for uploading images"""
    model = GalleryImage
    form = GalleryImageForm
    extra = 3  # Show 3 empty forms by default

    fields = ['image_preview', 'image', 'caption', 'display_order', 'is_cover']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px; border: 1px solid #ddd;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Preview"


class GalleryVideoInline(admin.TabularInline):
    """Simple inline for adding videos"""
    model = GalleryVideo
    form = GalleryVideoForm
    extra = 2  # Show 2 empty forms by default

    fields = ['video_url', 'title', 'description', 'display_order']

    def get_formset(self, request, obj=None, **kwargs):
        """Add help text to formset"""
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['video_url'].help_text = "Paste YouTube or Vimeo link"
        formset.form.base_fields['title'].help_text = "Enter video title"
        return formset


# ========== SIMPLE ADMIN CLASSES ==========

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    """Simple category admin"""
    list_display = ['name_display', 'display_order', 'total_events']
    list_editable = ['display_order']
    ordering = ['display_order']

    fields = ['name', 'description', 'display_order']

    def name_display(self, obj):
        return obj.get_name_display()

    name_display.short_description = "Category"

    def total_events(self, obj):
        return obj.events.count()

    total_events.short_description = "Events"


class GalleryEventForm(forms.ModelForm):
    """Simple event form"""

    class Meta:
        model = GalleryEvent
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'short_description': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Auto-fill short description if empty
        if not cleaned_data.get('short_description') and cleaned_data.get('description'):
            desc = cleaned_data['description'][:200]
            if len(cleaned_data['description']) > 200:
                desc += "..."
            cleaned_data['short_description'] = desc

        return cleaned_data


@admin.register(GalleryEvent)
class GalleryEventAdmin(admin.ModelAdmin):
    """Simple and user-friendly event admin"""
    form = GalleryEventForm

    # Simple list view
    list_display = [
        'title',
        'category',
        'event_date',
        'status_badge',
        'is_featured',
        'total_images_display',
        'total_videos_display'
    ]

    list_filter = ['category', 'status', 'is_featured', 'event_date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'event_date'

    # Add inlines for images and videos
    inlines = [GalleryImageInline, GalleryVideoInline]

    # Simple fieldsets for easy editing
    fieldsets = (
        (_('1. Basic Information'), {
            'fields': ('title', 'description', 'short_description'),
            'classes': ('wide',),
        }),
        (_('2. Event Details'), {
            'fields': ('event_date', 'location', 'category'),
            'classes': ('wide',),
        }),
        (_('3. Publish Settings'), {
            'fields': ('status', 'is_featured'),
            'classes': ('wide',),
            'description': _('Set "Published" to make visible on website')
        }),
    )

    # Make slug and timestamps read-only
    readonly_fields = ['slug', 'views_count', 'created_at', 'updated_at', 'published_at']

    # Custom display methods
    def status_badge(self, obj):
        colors = {
            'draft': '#6c757d',  # gray
            'published': '#198754',  # green
            'featured': '#fd7e14'  # orange
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )

    status_badge.short_description = "Status"

    def total_images_display(self, obj):
        count = obj.images.count()
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            '#198754' if count > 0 else '#6c757d',
            f"{count} 📷"
        )

    total_images_display.short_description = "Images"

    def total_videos_display(self, obj):
        count = obj.videos.count()
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            '#dc3545' if count > 0 else '#6c757d',
            f"{count} 📹"
        )

    total_videos_display.short_description = "Videos"

    # Simple admin actions
    actions = ['make_published', 'make_draft']

    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} events published successfully.')

    make_published.short_description = "Publish selected events"

    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} events moved to draft.')

    make_draft.short_description = "Move to draft"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Simple image admin"""

    # List view
    list_display = [
        'image_preview',
        'event',
        'caption_short',
        'is_cover_badge',
        'display_order',
        'created_date'
    ]

    list_filter = ['event', 'is_cover', 'event__category']
    search_fields = ['caption', 'event__title']
    list_editable = ['display_order']

    # Form
    form = GalleryImageForm

    # Custom fields
    fields = ['event', 'image', 'caption', 'display_order', 'is_cover']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 80px; border: 1px solid #ddd;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Image"

    def caption_short(self, obj):
        if obj.caption:
            return obj.caption[:30] + ('...' if len(obj.caption) > 30 else '')
        return "-"

    caption_short.short_description = "Caption"

    def is_cover_badge(self, obj):
        if obj.is_cover:
            return format_html(
                '<span style="background-color: #198754; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px;">COVER</span>'
            )
        return "-"

    is_cover_badge.short_description = "Cover"

    def created_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')

    created_date.short_description = "Created"


@admin.register(GalleryVideo)
class GalleryVideoAdmin(admin.ModelAdmin):
    """Simple video admin"""

    list_display = [
        'title',
        'event',
        'platform_badge',
        'display_order',
        'created_date'
    ]

    list_filter = ['event', 'platform', 'event__category']
    search_fields = ['title', 'description', 'event__title']
    list_editable = ['display_order']

    form = GalleryVideoForm

    fields = ['event', 'video_url', 'title', 'description', 'display_order']

    def platform_badge(self, obj):
        colors = {
            'youtube': '#dc3545',  # red
            'vimeo': '#1ab7ea',  # blue
            'other': '#6c757d'  # gray
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px;">{}</span>',
            colors.get(obj.platform, '#6c757d'),
            obj.get_platform_display().upper()
        )

    platform_badge.short_description = "Platform"

    def created_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')

    created_date.short_description = "Created"


# ========== ADMIN SITE CONFIGURATION ==========

# Customize admin site headers
admin.site.site_header = "📸 NKSC Gallery Management"
admin.site.site_title = "NKSC Gallery Admin"
admin.site.index_title = "🎯 Welcome to NKSC Gallery Dashboard"