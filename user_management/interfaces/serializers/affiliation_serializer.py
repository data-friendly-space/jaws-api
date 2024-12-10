from rest_framework import serializers

from user_management.models import Affiliation


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = ['id', 'name']

