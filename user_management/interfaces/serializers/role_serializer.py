from rest_framework import serializers

from user_management.models import UiConfiguration


class UiConfigurationTO(serializers.ModelSerializer):
    class Meta:
        model = UiConfiguration
        fields = ['color']
