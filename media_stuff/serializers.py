from rest_framework import serializers
from .models import GalleryCategory, GalleryEvent, GalleryImage, GalleryVideo


class GalleryCategorySerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    total_events = serializers.IntegerField(read_only=True)

    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug', 'description', 'name_display', 'total_events']


class GalleryImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = ['id', 'image_url', 'caption', 'display_order', 'is_cover', 'created_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            try:
                return request.build_absolute_uri(obj.image.url)
            except:
                return None
        return None


class GalleryVideoSerializer(serializers.ModelSerializer):
    embed_url = serializers.CharField(read_only=True)
    thumbnail_url = serializers.CharField(read_only=True)

    class Meta:
        model = GalleryVideo
        fields = ['id', 'title', 'description', 'video_url', 'embed_url', 'thumbnail_url', 'display_order',
                  'created_at']


class GalleryEventListSerializer(serializers.ModelSerializer):
    category_detail = GalleryCategorySerializer(source='category', read_only=True)
    cover_image = serializers.SerializerMethodField()
    year = serializers.IntegerField(source='event_date.year', read_only=True)
    total_images = serializers.IntegerField(read_only=True)
    total_videos = serializers.IntegerField(read_only=True)

    class Meta:
        model = GalleryEvent
        fields = [
            'id', 'title', 'slug', 'short_description',
            'event_date', 'location', 'year',
            'category', 'category_detail', 'is_featured',
            'total_images', 'total_videos', 'cover_image',
            'views_count'
        ]

    def get_cover_image(self, obj):
        request = self.context.get('request')
        cover = obj.cover_image
        if cover and request:
            try:
                return request.build_absolute_uri(cover.image.url)
            except:
                pass

        # Try to get first video thumbnail if no images
        first_video = obj.videos.first()
        if first_video and first_video.thumbnail_url:
            return first_video.thumbnail_url

        return None


class GalleryEventSerializer(serializers.ModelSerializer):
    category_detail = GalleryCategorySerializer(source='category', read_only=True)
    images = GalleryImageSerializer(many=True, read_only=True)
    videos = GalleryVideoSerializer(many=True, read_only=True)
    year = serializers.IntegerField(source='event_date.year', read_only=True)
    total_images = serializers.IntegerField(read_only=True)
    total_videos = serializers.IntegerField(read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = GalleryEvent
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'event_date', 'location', 'category', 'category_detail',
            'status', 'is_featured', 'views_count', 'year',
            'total_images', 'total_videos', 'cover_image',
            'images', 'videos', 'created_at', 'updated_at'
        ]

    def get_cover_image(self, obj):
        request = self.context.get('request')
        cover = obj.cover_image
        if cover and request:
            try:
                return request.build_absolute_uri(cover.image.url)
            except:
                pass
        return None