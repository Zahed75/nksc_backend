from rest_framework import serializers
from .models import (
    AboutSection, TimelineEvent, Director, 
    Facility, Statistic, ContactInfo
)


class AboutSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = [
            'id', 'title', 'subtitle', 'content', 
            'section_type', 'icon', 'display_order',
            'created_at', 'updated_at'
        ]


class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = [
            'id', 'year', 'title', 'description',
            'icon', 'display_order', 'image'
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        if request and instance.image:
            data['image'] = request.build_absolute_uri(instance.image.url)
        
        return data


class DirectorSerializer(serializers.ModelSerializer):
    is_current = serializers.ReadOnlyField()
    
    class Meta:
        model = Director
        fields = [
            'id', 'name', 'position', 'director_type', 'period',
            'bio', 'qualifications', 'email', 'phone', 'image',
            'website', 'linkedin', 'is_current', 'display_order',
            'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        if request and instance.image:
            data['image'] = request.build_absolute_uri(instance.image.url)
        
        return data


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = [
            'id', 'title', 'description', 'icon',
            'location', 'room_number', 'capacity',
            'display_order', 'image'
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        if request and instance.image:
            data['image'] = request.build_absolute_uri(instance.image.url)
        
        return data


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ['id', 'label', 'value', 'prefix', 'suffix', 'icon', 'display_order']


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['id', 'contact_type', 'label', 'value', 'icon', 'display_order']