"""This module contains the analysis model"""
from django.db import models

from analysis.models.administrative_division import AdministrativeDivision
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector


class Analysis(models.Model):
    """Analysis model"""
    workspace = models.ForeignKey(
        "user_management.Workspace",
        on_delete=models.CASCADE,
        related_name="analyses"
    )
    title = models.CharField(max_length=255, unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField()
    disaggregations = models.ManyToManyField(Disaggregation, blank=True)
    sectors = models.ManyToManyField(Sector)
    objectives = models.CharField(max_length=400)
    creator = models.ForeignKey('user_management.User', on_delete=models.CASCADE)
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
