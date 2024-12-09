"""This module contains the analysis model"""
from django.db import models

from analysis.models.administrative_division import AdministrativeDivision
from analysis.models.analysis_framework import AnalysisFramework
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector


class Analysis(models.Model):
    """Analysis model"""
    id = models.CharField(primary_key=True, max_length=36)
    title = models.CharField(max_length=255)
    analysis_framework = models.ForeignKey(AnalysisFramework, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField()
    disaggregations = models.ManyToManyField(Disaggregation, blank=True)
    sectors = models.ManyToManyField(Sector)
    objectives = models.CharField(max_length=400)
    workspace_id = models.CharField(max_length=36)
    creator = models.CharField(max_length=36)
    created_on = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)
    locations = models.ManyToManyField(AdministrativeDivision)

    class Meta:
        """Table metadata"""
        db_table = 'analysis'

    def get_all_locations_with_hierarchy(self):
        """Get all related locations with their hierarchies"""
        locations_with_hierarchy = {}
        for location in self.locations.all():
            locations_with_hierarchy[location.id] = location.get_hierarchy()
        return locations_with_hierarchy
