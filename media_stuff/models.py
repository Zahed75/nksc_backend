from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid


class GalleryCategory(models.Model):
    CATEGORY_CHOICES = [
        ('seminar', 'সেমিনার (Seminar)'),
        ('workshop', 'ওয়ার্কশপ (Workshop)'),
        ('conference', 'কনফারেন্স (Conference)'),
        ('cultural', 'সাংস্কৃতিক অনুষ্ঠান (Cultural Event)'),
        ('award', 'পুরস্কার বিতরণী (Award Ceremony)'),
        ('training', 'প্রশিক্ষণ (Training)'),
        ('other', 'অন্যান্য (Other)'),
    ]
    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='pi-images')
    color = models.CharField(max_length=20, default='bg-blue-100 text-blue-800')
    
    class Meta:
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.get_name_display()


class GalleryEvent(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('featured', 'Featured'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    short_description = models.TextField(max_length=200)
    
    # Event Details
    event_date = models.DateField()
    location = models.CharField(max_length=255)
    participants = models.IntegerField(default=0)
    organizer = models.CharField(max_length=100, blank=True)
    
    # Categorization
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, related_name='events')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    
    # SEO Metadata
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Gallery Event"
        verbose_name_plural = "Gallery Events"
        ordering = ['-event_date', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from title
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while GalleryEvent.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Update published_at if status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def year(self):
        return self.event_date.year
    
    @property
    def total_images(self):
        return self.images.count()
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class GalleryImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(GalleryEvent, on_delete=models.CASCADE, related_name='images')
    
    # Image Details
    image = models.ImageField(upload_to='gallery/images/')
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    
    # Ordering
    display_order = models.PositiveIntegerField(default=0)
    
    # Metadata
    uploaded_by = models.CharField(max_length=100, blank=True)
    is_cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return f"{self.event.title} - {self.caption or 'Image'}"
    
    def save(self, *args, **kwargs):
        # If this is set as cover, unset other covers for this event
        if self.is_cover:
            GalleryImage.objects.filter(event=self.event, is_cover=True).update(is_cover=False)
        
        # Auto-generate alt text if not provided
        if not self.alt_text and self.caption:
            self.alt_text = self.caption
        
        super().save(*args, **kwargs)


class GalleryStat(models.Model):
    """Store statistics about the gallery"""
    total_events = models.PositiveIntegerField(default=0)
    total_images = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    
    # Category counts
    seminar_count = models.PositiveIntegerField(default=0)
    workshop_count = models.PositiveIntegerField(default=0)
    conference_count = models.PositiveIntegerField(default=0)
    cultural_count = models.PositiveIntegerField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Gallery Statistic"
        verbose_name_plural = "Gallery Statistics"
    
    def __str__(self):
        return f"Gallery Stats - {self.last_updated.strftime('%Y-%m-%d %H:%M')}"