from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class AboutSection(models.Model):
    """About page sections"""
    SECTION_TYPES = [
        ('history', 'ইতিহাস (History)'),
        ('development', 'প্রাতিষ্ঠানিক উন্নয়ন (Development)'),
        ('recognition', 'স্বীকৃতি (Recognition)'),
        ('mission', 'অভিলক্ষ্য (Mission)'),
        ('vision', 'দৃষ্টিভঙ্গি (Vision)'),
        ('facilities', 'সুবিধা (Facilities)'),
        ('directors', 'পরিচালক (Directors)'),
        ('timeline', 'সময়রেখা (Timeline)'),
    ]
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    content = RichTextField()
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES)
    icon = models.CharField(max_length=50, default='pi-info-circle')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"
    
    def __str__(self):
        return f"{self.title} ({self.get_section_type_display()})"


class TimelineEvent(models.Model):
    """Timeline events for about page"""
    year = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='pi-calendar')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Optional image
    image = models.ImageField(upload_to='about/timeline/', blank=True, null=True)
    
    class Meta:
        ordering = ['-display_order', 'year']
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"
    
    def __str__(self):
        return f"{self.year} - {self.title}"


class Director(models.Model):
    """Directors of the center"""
    DIRECTOR_TYPES = [
        ('current', 'বর্তমান পরিচালক (Current)'),
        ('previous', 'সাবেক পরিচালক (Previous)'),
    ]
    
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    director_type = models.CharField(max_length=50, choices=DIRECTOR_TYPES, default='current')
    period = models.CharField(max_length=100, help_text="e.g., ২০২০ - ২০২৫")
    
    # Detailed info
    bio = RichTextField(blank=True)
    qualifications = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Image
    image = models.ImageField(upload_to='about/directors/', blank=True, null=True)
    
    # Social links
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    
    # Display
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['director_type', '-display_order', 'name']
        verbose_name = "Director"
        verbose_name_plural = "Directors"
    
    def __str__(self):
        return f"{self.name} ({self.position})"
    
    @property
    def is_current(self):
        return self.director_type == 'current'


class Facility(models.Model):
    """Facilities/amenities of the center"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='pi-building')
    
    # Optional details
    location = models.CharField(max_length=200, blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    capacity = models.CharField(max_length=50, blank=True, help_text="e.g., 50 persons, 1000 books")
    
    # Display
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Image
    image = models.ImageField(upload_to='about/facilities/', blank=True, null=True)
    
    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
        verbose_name_plural = "Facilities"
    
    def __str__(self):
        return self.title


class Statistic(models.Model):
    """Statistics/numbers for about page"""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    prefix = models.CharField(max_length=10, blank=True, help_text="e.g., +")
    suffix = models.CharField(max_length=10, blank=True, help_text="e.g., +, yrs")
    icon = models.CharField(max_length=50, default='pi-chart-line')
    
    # Display
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', 'label']
        verbose_name = "Statistic"
        verbose_name_plural = "Statistics"
    
    def __str__(self):
        return f"{self.label}: {self.value}"


class ContactInfo(models.Model):
    """Contact information for about page"""
    CONTACT_TYPES = [
        ('address', 'ঠিকানা'),
        ('email', 'ইমেইল'),
        ('phone', 'ফোন'),
        ('fax', 'ফ্যাক্স'),
        ('office_hours', 'অফিস সময়'),
    ]
    
    contact_type = models.CharField(max_length=50, choices=CONTACT_TYPES)
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', 'contact_type']
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return f"{self.label}: {self.value}"