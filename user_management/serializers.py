from rest_framework import serializers
from rest_framework import serializers
from .models import Chairman


class ChairmanSerializer(serializers.ModelSerializer):
    """Serializer for Chairman model - Only for GET API"""

    qualifications_list = serializers.SerializerMethodField()
    current_positions_list = serializers.SerializerMethodField()
    previous_positions_list = serializers.SerializerMethodField()

    class Meta:
        model = Chairman
        fields = [
            'id',
            'name_bangla',
            'name_english',
            'designation_bangla',
            'designation_english',
            'bio_bangla',
            'bio_english',
            'qualifications',
            'qualifications_list',
            'current_positions',
            'current_positions_list',
            'previous_positions',
            'previous_positions_list',
            'email',
            'phone',
            'profile_image',
            'signature_image',
            'is_active',
            'display_order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields  # All fields are read-only in API

    def get_qualifications_list(self, obj):
        return obj.get_qualifications_list()

    def get_current_positions_list(self, obj):
        return obj.get_current_positions_list()

    def get_previous_positions_list(self, obj):
        return obj.get_previous_positions_list()

    def to_representation(self, instance):
        """Add absolute URLs for media files"""
        data = super().to_representation(instance)
        request = self.context.get('request')

        # Add absolute URLs for media files
        if instance.profile_image and request:
            data['profile_image'] = request.build_absolute_uri(instance.profile_image.url)
        else:
            data['profile_image'] = None

        if instance.signature_image and request:
            data['signature_image'] = request.build_absolute_uri(instance.signature_image.url)
        else:
            data['signature_image'] = None

        return data
