from rest_framework import serializers
from .models import JournalPage


class JournalSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    preview_image_url = serializers.SerializerMethodField()

    class Meta:
        model = JournalPage
        fields = [
            'id', 'title', 'volume', 'year', 'issue', 'editor', 'issn',
            'description', 'pages', 'file_size_mb', 'doi_url',
            'download_url', 'preview_image_url'
        ]

    def get_download_url(self, obj):
        if obj.journal_file:
            return obj.journal_file.file.url
        return None

    def get_preview_image_url(self, obj):
        if obj.preview_image:
            return obj.preview_image.file.url
        return None
