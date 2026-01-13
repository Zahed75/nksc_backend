from rest_framework import serializers
from .models import Journal


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.pdf_file and request:
            data["pdf_file"] = request.build_absolute_uri(instance.pdf_file.url)
        else:
            data["pdf_file"] = None

        if instance.preview_image and request:
            data["preview_image"] = request.build_absolute_uri(instance.preview_image.url)
        else:
            data["preview_image"] = None

        return data
