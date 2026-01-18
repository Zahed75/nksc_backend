from django.db import models
from django.utils.text import slugify


class Department(models.Model):
    """Staff department/category"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='pi-users', help_text='PrimeNG icon class')
    color = models.CharField(max_length=50, default='bg-blue-100 text-blue-800')
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Department"
        verbose_name_plural = "Departments"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    @property
    def staff_count(self):
        # FIXED: Use the correct related_name 'staff' (singular)
        return self.staff.filter(is_active=True).count()


class Staff(models.Model):
    """Staff/Employee model"""
    DESIGNATION_CHOICES = [
        ('professor', 'অধ্যাপক (Professor)'),
        ('associate_professor', 'সহযোগী অধ্যাপক (Associate Professor)'),
        ('assistant_professor', 'সহকারী অধ্যাপক (Assistant Professor)'),
        ('lecturer', 'প্রভাষক (Lecturer)'),
        ('research_fellow', 'গবেষণা ফেলো (Research Fellow)'),
        ('research_assistant', 'গবেষণা সহকারী (Research Assistant)'),
        ('administrative_officer', 'প্রশাসনিক কর্মকর্তা (Administrative Officer)'),
        ('accountant', 'হিসাবরক্ষক (Accountant)'),
        ('librarian', 'গ্রন্থাগারিক (Librarian)'),
        ('technical_staff', 'প্রযুক্তিগত কর্মী (Technical Staff)'),
        ('support_staff', 'সাহায্যকারী কর্মী (Support Staff)'),
        ('other', 'অন্যান্য (Other)'),
    ]
    
    # Personal Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    
    # Contact Information
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    alternate_phone = models.CharField(max_length=20, blank=True)
    
    # Professional Details
    bio = models.TextField(blank=True, help_text="Short biography/description")
    qualifications = models.TextField(blank=True, help_text="Educational qualifications")
    research_interests = models.TextField(blank=True, help_text="Research interests")
    
    # Media
    profile_image = models.ImageField(upload_to='staff/profiles/', blank=True, null=True)
    cv = models.FileField(upload_to='staff/cvs/', blank=True, null=True, help_text="PDF format preferred")
    
    # Social Links
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    google_scholar = models.URLField(blank=True)
    researchgate = models.URLField(blank=True)
    orcid = models.CharField(max_length=50, blank=True)
    
    # Office Details
    office_room = models.CharField(max_length=50, blank=True)
    office_hours = models.TextField(blank=True, help_text="Office hours/days")
    
    # Status
    is_active = models.BooleanField(default=True)
    join_date = models.DateField(null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    
    # SEO Metadata
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Staff"
        verbose_name_plural = "Staff"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from name
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Staff.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Auto-generate meta fields if empty
        if not self.meta_title:
            self.meta_title = f"{self.name} - {self.get_designation_display()}"
        if not self.meta_description and self.bio:
            self.meta_description = self.bio[:160]  # First 160 characters
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.get_designation_display()})"
    
    @property
    def full_title(self):
        """Get full title with designation"""
        return f"{self.get_designation_display()} {self.name}"
    
    @property
    def display_phone(self):
        """Format phone number for display"""
        if self.phone:
            return self.phone
        return "Not available"
    
    @property
    def years_of_service(self):
        """Calculate years of service"""
        if self.join_date:
            from datetime import date
            today = date.today()
            return today.year - self.join_date.year
        return None


class StaffEducation(models.Model):
    """Staff education history"""
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    year = models.CharField(max_length=20, help_text="e.g., 2010-2014, 2020")
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-year', 'display_order']
        verbose_name = "Staff Education"
        verbose_name_plural = "Staff Education"
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"


class StaffExperience(models.Model):
    """Staff work experience"""
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='experience')
    position = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'display_order']
        verbose_name = "Staff Experience"
        verbose_name_plural = "Staff Experience"
    
    def __str__(self):
        return f"{self.position} at {self.organization}"
    
    @property
    def duration(self):
        """Calculate duration in years"""
        from datetime import date
        end = self.end_date if self.end_date else date.today()
        
        years = end.year - self.start_date.year
        months = end.month - self.start_date.month
        
        if months < 0:
            years -= 1
            months += 12
        
        if years == 0:
            return f"{months} months"
        elif months == 0:
            return f"{years} years"
        else:
            return f"{years} years {months} months"