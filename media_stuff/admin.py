from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import GalleryCategory, GalleryEvent, GalleryImage, GalleryStat


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ('image', 'thumbnail_preview', 'caption', 'alt_text', 'display_order', 'is_cover')
    readonly_fields = ('thumbnail_preview',)
    
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', obj.image.url)
        return "No image"
    thumbnail_preview.short_description = 'Preview'


class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_display', 'slug', 'event_count', 'icon', 'color_display')
    list_display_links = ('name_display', 'slug')
    search_fields = ('name',)
    readonly_fields = ('slug',)
    
    def name_display(self, obj):
        return obj.get_name_display()
    name_display.short_description = 'Category Name'
    
    def event_count(self, obj):
        return obj.events.count()
    event_count.short_description = 'Events'
    
    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 4px;">{}</span>',
            obj.color.split(' ')[0].replace('bg-', ''),
            obj.color
        )
    color_display.short_description = 'Color'


class GalleryEventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'category_display', 
        'event_date', 
        'location', 
        'participants', 
        'status_badge', 
        'is_featured_display',
        'images_count',
        'views_count'
    )
    list_display_links = ('title',)
    list_filter = ('category', 'status', 'is_featured', 'event_date')
    search_fields = ('title', 'description', 'location', 'organizer')
    # FIXED: Removed list_editable since fields need to be in list_display
    readonly_fields = ('slug', 'views_count', 'created_at', 'updated_at', 'published_at', 'images_count_display')
    prepopulated_fields = {}
    date_hierarchy = 'event_date'
    inlines = [GalleryImageInline]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'slug', 'description', 'short_description')
        }),
        (_('Event Details'), {
            'fields': ('event_date', 'location', 'participants', 'organizer', 'category')
        }),
        (_('Status & Visibility'), {
            'fields': ('status', 'is_featured', 'views_count')
        }),
        (_('SEO Metadata'), {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
        (_('Images'), {
            'fields': ('images_count_display',),
            'classes': ('collapse',)
        }),
    )
    
    def category_display(self, obj):
        return obj.category.get_name_display() if obj.category else '-'
    category_display.short_description = 'Category'
    
    def status_badge(self, obj):
        colors = {
            'draft': 'gray',
            'published': 'green',
            'featured': 'orange'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def is_featured_display(self, obj):
        if obj.is_featured:
            return format_html('<span style="color: orange;">★</span> Featured')
        return format_html('<span style="color: gray;">-</span>')
    is_featured_display.short_description = 'Featured'
    
    def images_count(self, obj):
        return obj.images.count()
    images_count.short_description = 'Images'
    
    def images_count_display(self, obj):
        return f"{obj.images.count()} images"
    images_count_display.short_description = 'Total Images'
    
    actions = ['make_published', 'make_featured', 'make_draft']
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} events published successfully.')
    make_published.short_description = "Mark selected events as published"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} events marked as featured.')
    make_featured.short_description = "Mark selected events as featured"
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} events marked as draft.')
    make_draft.short_description = "Mark selected events as draft"


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_display', 'event', 'caption', 'is_cover', 'display_order', 'created_at')
    list_display_links = ('thumbnail_display', 'caption')
    list_filter = ('event', 'is_cover', 'created_at')
    search_fields = ('caption', 'alt_text', 'event__title')
    # FIXED: Only keep display_order as editable since is_cover is not in list_display
    list_editable = ('display_order',)
    readonly_fields = ('created_at', 'thumbnail_display')
    
    def thumbnail_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No image"
    thumbnail_display.short_description = 'Thumbnail'


class GalleryStatAdmin(admin.ModelAdmin):
    list_display = ('total_events', 'total_images', 'total_views', 'last_updated')
    readonly_fields = ('last_updated',)
    
    def has_add_permission(self, request):
        # Only one stats object should exist
        return not GalleryStat.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


# Register models
admin.site.register(GalleryCategory, GalleryCategoryAdmin)
admin.site.register(GalleryEvent, GalleryEventAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(GalleryStat, GalleryStatAdmin)