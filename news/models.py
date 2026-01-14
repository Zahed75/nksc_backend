from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField  # Add this import


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "News Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class News(models.Model):
    URGENCY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('breaking', 'Breaking News'),
    ]
    
    LANGUAGE_CHOICES = [
        ('bn', 'বাংলা (Bangla)'),
        ('en', 'English'),
        ('hi', 'हिन्दी (Hindi)'),
        ('ar', 'عربى (Arabic)'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    short_description = RichTextField()  # Changed to RichTextField
    content = RichTextField()  # Already RichTextField
    
    # Category and tags
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma separated tags")
    
    # Urgency and language
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='normal')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='bn')
    
    # Event/Session fields
    is_event = models.BooleanField(default=False)
    event_date = models.DateField(null=True, blank=True)
    event_location = models.CharField(max_length=255, blank=True)
    event_speakers = models.TextField(blank=True, help_text="Comma separated speaker names")
    
    # Research related
    is_research = models.BooleanField(default=False)
    research_topic = models.CharField(max_length=255, blank=True)
    research_department = models.CharField(max_length=100, blank=True)
    
    # Media files
    thumbnail_image = models.ImageField(upload_to='news/thumbnails/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='news/banners/', blank=True, null=True)
    attachment_file = models.FileField(upload_to='news/attachments/', blank=True, null=True)
    
    # Metadata
    author = models.CharField(max_length=100, default='গবেষণা বিভাগ (Research Department)')
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    views_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "News"
        ordering = ['-publish_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []