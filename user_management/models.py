from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=50,
        choices=[
            ("admin", "Admin"),
            ("editor", "Editor"),
            ("viewer", "Viewer"),
        ],
        default="viewer",
    )

    def __str__(self):
        return self.user.username


class Chairman(models.Model):
    """Model for storing current chairman information - All CRUD through admin"""

    # Personal Information
    name_bangla = models.CharField(
        max_length=255,
        verbose_name='নাম (বাংলা)',
        help_text='চেয়ারম্যানের পূর্ণ নাম বাংলায়'
    )

    name_english = models.CharField(
        max_length=255,
        verbose_name='Name (English)',
        help_text='Full name in English'
    )

    # Designation/Titles
    designation_bangla = models.CharField(
        max_length=255,
        verbose_name='পদবী (বাংলা)',
        help_text='উদাহরণ: পরিচালক, নাজমুল করিম স্টাডি সেন্টার'
    )

    designation_english = models.CharField(
        max_length=255,
        verbose_name='Designation (English)',
        help_text='Example: Director, Nazmul Karim Study Center'
    )

    # Biography
    bio_bangla = models.TextField(
        verbose_name='সংক্ষিপ্ত পরিচিতি (বাংলা)',
        help_text='চেয়ারম্যানের সংক্ষিপ্ত জীবনবৃত্তান্ত বাংলায়'
    )

    bio_english = models.TextField(
        verbose_name='Brief Biography (English)',
        help_text='Brief biography in English',
        default=False,
        null=True,
    )

    # Qualifications
    qualifications = models.TextField(
        verbose_name='Academic Qualifications',
        help_text='List academic qualifications (one per line)',
        blank=True
    )

    # Positions
    current_positions = models.TextField(
        verbose_name='Current Positions',
        help_text='Current positions held (one per line)',
        blank=True
    )

    previous_positions = models.TextField(
        verbose_name='Previous Positions',
        help_text='Previous important positions (one per line)',
        blank=True
    )

    # Contact
    email = models.EmailField(verbose_name='Email Address', blank=True)
    phone = models.CharField(max_length=50, verbose_name='Phone Number', blank=True)

    # Images
    profile_image = models.ImageField(
        upload_to='chairman/',
        verbose_name='Profile Photo',
        blank=True,
        null=True
    )

    signature_image = models.ImageField(
        upload_to='chairman/signature/',
        verbose_name='Signature',
        blank=True,
        null=True
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
        help_text='Show this chairman on the website'
    )

    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
        help_text='Lower numbers display first'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Chairman'
        verbose_name_plural = 'Chairmen'
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.name_english} - {self.designation_english}"

    def get_qualifications_list(self):
        """Return qualifications as list"""
        if self.qualifications:
            return [q.strip() for q in self.qualifications.split('\n') if q.strip()]
        return []

    def get_current_positions_list(self):
        """Return current positions as list"""
        if self.current_positions:
            return [p.strip() for p in self.current_positions.split('\n') if p.strip()]
        return []

    def get_previous_positions_list(self):
        """Return previous positions as list"""
        if self.previous_positions:
            return [p.strip() for p in self.previous_positions.split('\n') if p.strip()]
        return []
