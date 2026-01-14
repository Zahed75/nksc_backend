from rest_framework import serializers
from .models import News, NewsCategory
from django.conf import settings


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name', 'slug', 'description']


class NewsSerializer(serializers.ModelSerializer):
    category_detail = NewsCategorySerializer(source='category', read_only=True)
    tags_list = serializers.SerializerMethodField()
    days_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'short_description', 'content',
            'category', 'category_detail', 'tags', 'tags_list',
            'urgency', 'language', 'is_event', 'event_date', 
            'event_location', 'event_speakers', 'is_research',
            'research_topic', 'research_department',
            'thumbnail_image', 'banner_image', 'attachment_file',
            'author', 'is_published', 'publish_date', 'views_count',
            'created_at', 'updated_at', 'days_ago'
        ]
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
    
    def get_days_ago(self, obj):
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        return delta.days
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        # Build absolute URLs for media files
        if request:
            if instance.thumbnail_image:
                data['thumbnail_image'] = request.build_absolute_uri(instance.thumbnail_image.url)
            if instance.banner_image:
                data['banner_image'] = request.build_absolute_uri(instance.banner_image.url)
            if instance.attachment_file:
                data['attachment_file'] = request.build_absolute_uri(instance.attachment_file.url)
        
        return data


class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'title', 'short_description', 'content',
            'category', 'tags', 'urgency', 'language',
            'is_event', 'event_date', 'event_location', 'event_speakers',
            'is_research', 'research_topic', 'research_department',
            'thumbnail_image', 'banner_image', 'attachment_file',
            'author', 'is_published', 'publish_date'
        ]
    
    def validate_slug(self, value):
        # Auto-generate slug from title if not provided
        if not value:
            from django.utils.text import slugify
            value = slugify(self.initial_data.get('title', ''))
        
        # Ensure slug is unique
        queryset = News.objects.filter(slug=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("A news with this slug already exists.")
        
        return value