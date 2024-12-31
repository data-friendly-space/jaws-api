"""Request object to create an analysis contract"""
from rest_framework import serializers


class CreatePresignedUrlUploadFileIn(serializers.Serializer):
    """Request input for an analysis creation"""
    filename = serializers.CharField()
    analysis_id = serializers.IntegerField()
    size_bytes = serializers.IntegerField()
