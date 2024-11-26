from rest_framework import serializers
from analysis.models.analysis import Analysis
from app.core.serializer.CamelCaseMixin import CamelCaseMixin

class AnalysisSerializer(CamelCaseMixin, serializers.ModelSerializer):
    """
    Serializer to transform Analysis model to AnalysisTO format.
    """
    id = serializers.CharField(max_length=36, read_only=True)
    title = serializers.CharField(max_length=255)
    start_date = serializers.DateField(allow_null=True, required=False)
    end_date = serializers.DateField()
    objetives = serializers.CharField(max_length=400)
    workspace_id = serializers.CharField(max_length=36)
    creator = serializers.CharField(max_length=36)
    created_on = serializers.DateTimeField()
    last_change = serializers.DateTimeField()
    disaggregations = serializers.SerializerMethodField()
    sectors = serializers.SerializerMethodField()

    class Meta:
        """from where it takes the fields"""
        model = Analysis
        fields = [
                    'id', 'title', 'start_date', 'end_date',
                    'objetives', 'workspace_id', 'creator',
                    'created_on', 'last_change', 'disaggregations', 
                    'sectors'
                ]

    def get_disaggregations(self, obj):
        '''serialize disaggregations'''
        if obj.disaggregations:
            return [disaggregation.id for disaggregation in obj.disaggregations]

    def get_sectors(self, obj):
        '''serialize sectors]'''
        if obj.sectors:
            return [sector.id for sector in obj.sectors]
