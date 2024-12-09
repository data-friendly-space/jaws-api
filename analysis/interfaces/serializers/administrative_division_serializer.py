"""This module contains the disaggregation serializer"""

from rest_framework import serializers

from analysis.models.administrative_division import AdministrativeDivision
from common.serializer.CamelCaseMixin import CamelCaseMixin


class AdministrativeDivisionSerializer(CamelCaseMixin, serializers.ModelSerializer):
    """
    Serializer to transform Analysis model to AnalysisTO format.
    """

    p_code = serializers.CharField()
    name = serializers.CharField()
    hierarchy = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        """Base class"""

        model = AdministrativeDivision
        fields = ["p_code", "name", "hierarchy"]

    def get_hierarchy(self, obj):
        """Serialize locations with hierarchy"""
        try:
            if not obj.hierarchy:
                return
            return [
                {
                    "adminLevel": loc["adminLevel"],
                    "name": loc["name"],
                    "pCode": loc["pCode"],
                }
                for loc in obj.hierarchy
            ]
        except AttributeError:
            return


    def to_representation(self, instance):
        """Customize representation to exclude null fields"""
        representation = super().to_representation(instance)
        if representation.get("hierarchy") is None:
            representation.pop("hierarchy", None)
        return representation
