from rest_framework import serializers
from .models import Department, Staff, StaffEducation, StaffExperience
from django.conf import settings


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 'display_order']
        read_only_fields = ['slug']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['staff_count'] = instance.staff_count
        return data


class StaffEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffEducation
        fields = ['id', 'degree', 'institution', 'year', 'description', 'display_order']


class StaffExperienceSerializer(serializers.ModelSerializer):
    duration = serializers.ReadOnlyField()
    
    class Meta:
        model = StaffExperience
        fields = ['id', 'position', 'organization', 'start_date', 'end_date', 'is_current', 'duration', 'description', 'display_order']


class StaffSerializer(serializers.ModelSerializer):
    department_detail = DepartmentSerializer(source='department', read_only=True)
    education = StaffEducationSerializer(many=True, read_only=True)
    experience = StaffExperienceSerializer(many=True, read_only=True)
    full_title = serializers.ReadOnlyField()
    years_of_service = serializers.ReadOnlyField()
    
    class Meta:
        model = Staff
        fields = [
            'id', 'name', 'slug', 'designation', 'department', 'department_detail',
            'full_title', 'email', 'phone', 'alternate_phone', 'bio', 
            'qualifications', 'research_interests', 'profile_image', 'cv',
            'website', 'linkedin', 'google_scholar', 'researchgate', 'orcid',
            'office_room', 'office_hours', 'is_active', 'join_date', 
            'years_of_service', 'display_order', 'education', 'experience',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        # Build absolute URLs for media files
        if request:
            if instance.profile_image:
                data['profile_image'] = request.build_absolute_uri(instance.profile_image.url)
            if instance.cv:
                data['cv'] = request.build_absolute_uri(instance.cv.url)
        
        # Add designation display text
        data['designation_display'] = instance.get_designation_display()
        
        return data


class StaffListSerializer(serializers.ModelSerializer):
    department_detail = DepartmentSerializer(source='department', read_only=True)
    designation_display = serializers.CharField(source='get_designation_display', read_only=True)
    
    class Meta:
        model = Staff
        fields = [
            'id', 'name', 'slug', 'designation', 'designation_display',
            'department', 'department_detail', 'email', 'phone', 'profile_image',
            'is_active', 'display_order'
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        if request and instance.profile_image:
            data['profile_image'] = request.build_absolute_uri(instance.profile_image.url)
        
        return data