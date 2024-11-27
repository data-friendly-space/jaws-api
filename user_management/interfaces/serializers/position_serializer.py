from rest_framework import serializers

from user_management.models import Position


class PositionTO(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']
