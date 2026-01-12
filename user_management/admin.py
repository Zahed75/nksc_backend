from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# If you have any custom user-related models (like UserProfile), import and register here
# from .models import UserProfile

# Register the default User model with Django admin
admin.site.unregister(User)  # Unregister default to customize if needed
admin.site.register(User, UserAdmin)

# Example: If you had UserProfile model linked to User
# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone_number', 'address')  # Adjust fields
#     search_fields = ('user__username', 'phone_number')
