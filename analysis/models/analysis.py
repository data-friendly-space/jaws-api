'''This module contains the analysis model'''
from django.db import models

from analysis.models.analysis_framework import AnalysisFramework
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector


class Analysis(models.Model):
    '''Analysis model'''
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

    class Meta:
        db_table = 'analysis'


