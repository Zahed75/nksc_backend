from rest_framework import serializers
from .models import GalleryCategory, GalleryEvent, GalleryImage
from django.conf import settings


class GalleryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name_display'] = instance.get_name_display()
        return data


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image_url', 'thumbnail_url', 'caption', 'alt_text', 'is_cover', 'display_order']
    
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        # Fallback to main image if no thumbnail
        return self.get_image_url(obj)


class GalleryEventSerializer(serializers.ModelSerializer):
    category_detail = GalleryCategorySerializer(source='category', read_only=True)
    images = GalleryImageSerializer(many=True, read_only=True)
    year = serializers.IntegerField(read_only=True)
    total_images = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = GalleryEvent
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'event_date', 'location', 'participants', 'organizer',
            'category', 'category_detail', 'status', 'is_featured',
            'views_count', 'year', 'total_images', 'images',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'views_count', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        # Format date for display
        if instance.event_date:
            data['date_display'] = instance.event_date.strftime('%d %B, %Y')
        
        # Get cover image
        cover_image = instance.images.filter(is_cover=True).first()
        if cover_image:
            data['cover_image'] = GalleryImageSerializer(cover_image, context={'request': request}).data
        
        # Get first 4 images for thumbnail preview
        preview_images = instance.images.all()[:4]
        data['preview_images'] = GalleryImageSerializer(preview_images, many=True, context={'request': request}).data
        
        return data


class GalleryEventListSerializer(serializers.ModelSerializer):
    category_detail = GalleryCategorySerializer(source='category', read_only=True)
    cover_image = serializers.SerializerMethodField()
    year = serializers.IntegerField(read_only=True)
    total_images = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = GalleryEvent
        fields = [
            'id', 'title', 'slug', 'short_description',
            'event_date', 'location', 'participants', 'year',
            'category', 'category_detail', 'is_featured',
            'total_images', 'cover_image', 'views_count'
        ]
    
    def get_cover_image(self, obj):
        request = self.context.get('request')
        cover_image = obj.images.filter(is_cover=True).first()
        if cover_image:
            if cover_image.thumbnail and request:
                return request.build_absolute_uri(cover_image.thumbnail.url)
            elif cover_image.image and request:
                return request.build_absolute_uri(cover_image.image.url)
        return None