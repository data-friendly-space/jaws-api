'''This module contains the analysis framework'''
from django.db import models


class AnalysisFramework(models.Model):
    '''Analysis Framework'''
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'analysis_framework'
