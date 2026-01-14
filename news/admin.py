from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import News, NewsCategory
from ckeditor.widgets import CKEditorWidget


# Custom form for News with CKEditor
class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = News
        fields = '__all__'  # This will include ALL fields including slug
        widgets = {
            'slug': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'slug', 'news_count')
    list_display_links = ('name', 'slug')
    search_fields = ('id','name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'description')
    
    def news_count(self, obj):
        return obj.news_set.count()
    news_count.short_description = 'News Count'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm  # Use the custom form with CKEditor
    
    list_display = (
        'title', 
        'category', 
        'urgency_display', 
        'language_display', 
        'is_published', 
        'publish_date', 
        'views_count'
    )
    list_display_links = ('title',)
    list_filter = (
        'category', 
        'urgency', 
        'language', 
        'is_published', 
        'is_event', 
        'is_research', 
        'publish_date'
    )
    search_fields = ('title', 'short_description', 'content', 'author', 'tags')
    list_editable = ('is_published',)
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}  # This will auto-generate slug from title
    date_hierarchy = 'publish_date'
    list_per_page = 20
    
    # Define fieldsets for better organization
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'slug', 'short_description', 'content')
        }),
        (_('Categorization'), {
            'fields': ('category', 'tags')
        }),
        (_('Status & Language'), {
            'fields': ('urgency', 'language')
        }),
        (_('Event Information'), {
            'fields': ('is_event', 'event_date', 'event_location', 'event_speakers'),
            'classes': ('collapse',)
        }),
        (_('Research Information'), {
            'fields': ('is_research', 'research_topic', 'research_department'),
            'classes': ('collapse',)
        }),
        (_('Media Files'), {
            'fields': ('thumbnail_image', 'banner_image', 'attachment_file')
        }),
        (_('Publication Information'), {
            'fields': ('author', 'is_published', 'publish_date')
        }),
        (_('Statistics'), {
            'fields': ('views_count',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Custom methods for display
    def urgency_display(self, obj):
        urgency_colors = {
            'normal': '🟢',
            'urgent': '🟠',
            'breaking': '🔴',
        }
        return format_html(
            '{} {}',
            urgency_colors.get(obj.urgency, '⚪'),
            obj.get_urgency_display()
        )
    urgency_display.short_description = 'Urgency'
    urgency_display.admin_order_field = 'urgency'
    
    def language_display(self, obj):
        language_icons = {
            'bn': '🇧🇩',
            'en': '🇬🇧',
            'hi': '🇮🇳',
            'ar': '🇸🇦',
        }
        return format_html(
            '{} {}',
            language_icons.get(obj.language, '🌐'),
            obj.get_language_display()
        )
    language_display.short_description = 'Language'
    language_display.admin_order_field = 'language'


# Register models
admin.site.register(NewsCategory, NewsCategoryAdmin)
admin.site.register(News, NewsAdmin)