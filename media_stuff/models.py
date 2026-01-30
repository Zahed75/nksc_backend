from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
import os


def gallery_image_path(instance, filename):
    """Generate path for gallery images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'gallery/events/{instance.event.id}/images/{filename}'


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
    description = models.TextField(blank=True, help_text="Brief description of this category")
    display_order = models.PositiveIntegerField(default=0, help_text="Order in which category appears")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()

    @property
    def total_events(self):
        return self.events.filter(status='published').count()


class GalleryEvent(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft - Not visible on website'),
        ('published', 'Published - Visible on website'),
        ('featured', 'Featured - Highlighted on website'),
    ]

    # Basic Information
    title = models.CharField(
        max_length=255,
        help_text="Title of the event (e.g., 'Annual Seminar 2023')"
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)

    # Event Details
    description = models.TextField(
        help_text="Full description of the event"
    )
    short_description = models.TextField(
        max_length=200,
        help_text="Brief description (max 200 characters) shown in listings"
    )
    event_date = models.DateField(
        help_text="Date when the event took place"
    )
    location = models.CharField(
        max_length=255,
        help_text="Venue location (e.g., 'NKSC Auditorium')"
    )

    # Categorization
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        help_text="Select event category"
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Check to feature this event on homepage"
    )

    # Statistics
    views_count = models.PositiveIntegerField(default=0, editable=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    published_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        verbose_name = "Gallery Event"
        verbose_name_plural = "Gallery Events"
        ordering = ['-event_date', '-created_at']

    def save(self, *args, **kwargs):
        # Generate slug if not exists
        if not self.slug:
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = f"event-{timezone.now().strftime('%Y%m%d')}"

            slug = base_slug
            counter = 1
            while GalleryEvent.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Auto-generate short description if empty
        if not self.short_description.strip():
            self.short_description = self.description[:200].strip()
            if len(self.description) > 200:
                self.short_description += "..."

        # Set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.event_date.year})"

    @property
    def year(self):
        return self.event_date.year

    @property
    def total_images(self):
        return self.images.count()

    @property
    def total_videos(self):
        return self.videos.count()

    @property
    def cover_image(self):
        """Get the first image marked as cover, or first image"""
        cover = self.images.filter(is_cover=True).first()
        if cover:
            return cover
        return self.images.first()

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class GalleryImage(models.Model):
    """Model for gallery images - Simple upload process"""

    event = models.ForeignKey(
        GalleryEvent,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="Select the event for these images"
    )

    # Single image upload
    image = models.ImageField(
        upload_to=gallery_image_path,
        help_text="Upload image (Recommended size: 1200x800px)"
    )

    # Simple caption
    caption = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional caption for the image"
    )

    # Display order
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order in which image appears (lower numbers first)"
    )

    # Cover image flag
    is_cover = models.BooleanField(
        default=False,
        help_text="Check to set as cover image for the event"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['display_order', 'created_at']

    def __str__(self):
        if self.caption:
            return f"Image: {self.caption}"
        return f"Image for {self.event.title}"

    def save(self, *args, **kwargs):
        # If this image is set as cover, unset other covers
        if self.is_cover:
            GalleryImage.objects.filter(
                event=self.event,
                is_cover=True
            ).exclude(id=self.id).update(is_cover=False)

        super().save(*args, **kwargs)


class GalleryVideo(models.Model):
    """Simple video model with just URL and caption"""

    VIDEO_PLATFORMS = [
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('other', 'Other'),
    ]

    event = models.ForeignKey(
        GalleryEvent,
        on_delete=models.CASCADE,
        related_name='videos',
        help_text="Select the event for this video"
    )

    # Simple URL field
    video_url = models.URLField(
        help_text="Paste YouTube or Vimeo video URL"
    )

    # Platform detection (auto-filled)
    platform = models.CharField(
        max_length=20,
        choices=VIDEO_PLATFORMS,
        default='youtube',
        editable=False
    )

    # Simple title/caption
    title = models.CharField(
        max_length=255,
        help_text="Title for the video"
    )

    # Optional description
    description = models.TextField(
        blank=True,
        help_text="Optional description for the video"
    )

    # Display order
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order in which video appears"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        ordering = ['display_order', 'created_at']

    def __str__(self):
        return f"Video: {self.title}"

    def save(self, *args, **kwargs):
        # Auto-detect platform from URL
        if 'youtube.com' in self.video_url or 'youtu.be' in self.video_url:
            self.platform = 'youtube'
        elif 'vimeo.com' in self.video_url:
            self.platform = 'vimeo'
        else:
            self.platform = 'other'

        super().save(*args, **kwargs)

    @property
    def video_id(self):
        """Extract video ID from URL"""
        import re

        if self.platform == 'youtube':
            patterns = [
                r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?]+)',
                r'youtube\.com/embed/([^&\n?]+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, self.video_url)
                if match:
                    return match.group(1)

        elif self.platform == 'vimeo':
            pattern = r'vimeo\.com/(?:video/)?(\d+)'
            match = re.search(pattern, self.video_url)
            if match:
                return match.group(1)

        return None

    @property
    def embed_url(self):
        """Get embed URL for the video"""
        video_id = self.video_id
        if not video_id:
            return None

        if self.platform == 'youtube':
            return f"https://www.youtube.com/embed/{video_id}"
        elif self.platform == 'vimeo':
            return f"https://player.vimeo.com/video/{video_id}"

        return None

    @property
    def thumbnail_url(self):
        """Get thumbnail URL"""
        video_id = self.video_id
        if not video_id:
            return None

        if self.platform == 'youtube':
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        elif self.platform == 'vimeo':
            # Vimeo thumbnails require API call
            return None

        return None