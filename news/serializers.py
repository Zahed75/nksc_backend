from rest_framework import serializers
from .models import News, NewsCategory
from django.conf import settings
from django.utils.text import slugify
import re


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name', 'slug', 'description']
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True, 'read_only': True}
        }
    
    def create(self, validated_data):
        name = validated_data.get('name', '')
        slug = slugify(name)
        
        base_slug = slug
        counter = 1
        while NewsCategory.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        validated_data['slug'] = slug
        return NewsCategory.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        if 'name' in validated_data and validated_data['name'] != instance.name:
            name = validated_data['name']
            slug = slugify(name)
            
            base_slug = slug
            counter = 1
            while NewsCategory.objects.filter(slug=slug).exclude(id=instance.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            validated_data['slug'] = slug
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


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
        extra_kwargs = {
            'slug': {'required': False, 'read_only': True}
        }
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
    
    def get_days_ago(self, obj):
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        return delta.days
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
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
    
    # FIXED INDENTATION - This was outside the class!
    def create(self, validated_data):
        # Auto-generate slug from title
        title = validated_data.get('title', '')
        
        # Generate slug using slugify
        slug = slugify(title)
        
        # If slugify returns empty (happens with certain Bengali characters)
        if not slug or slug.strip() == '':
            # Clean the title - remove special characters but keep Bengali
            clean_title = re.sub(r'[^\w\u0980-\u09FF\s-]', ' ', title)
            clean_title = re.sub(r'\s+', ' ', clean_title).strip()
            
            # Try slugify again with cleaned title
            slug = slugify(clean_title)
            
            # If still empty, create a simple slug
            if not slug or slug.strip() == '':
                # Take first few words and join with hyphens
                words = clean_title.split()[:4]  # Take first 4 words
                slug = '-'.join(words)[:50].lower()
                # Remove any non-alphanumeric characters except hyphens
                slug = re.sub(r'[^\w-]', '', slug)
        
        # If we still don't have a slug, use a timestamp-based one
        if not slug or slug.strip() == '':
            from django.utils import timezone
            slug = f"news-{timezone.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Ensure slug is not too long
        slug = slug[:100]
        
        # Ensure slug is unique
        base_slug = slug
        counter = 1
        while News.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Add the auto-generated slug to validated_data
        validated_data['slug'] = slug
        
        # Create and return the news object
        return News.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Auto-generate new slug if title is being updated
        if 'title' in validated_data and validated_data['title'] != instance.title:
            title = validated_data['title']
            
            # Generate new slug
            slug = slugify(title)
            
            if not slug or slug.strip() == '':
                clean_title = re.sub(r'[^\w\u0980-\u09FF\s-]', ' ', title)
                clean_title = re.sub(r'\s+', ' ', clean_title).strip()
                slug = slugify(clean_title)
                
                if not slug or slug.strip() == '':
                    words = clean_title.split()[:4]
                    slug = '-'.join(words)[:50].lower()
                    slug = re.sub(r'[^\w-]', '', slug)
            
            if not slug or slug.strip() == '':
                from django.utils import timezone
                slug = f"news-updated-{timezone.now().strftime('%Y%m%d-%H%M%S')}"
            
            slug = slug[:100]
            
            # Ensure slug is unique (excluding current instance)
            base_slug = slug
            counter = 1
            while News.objects.filter(slug=slug).exclude(id=instance.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            validated_data['slug'] = slug
        
        # Update the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance