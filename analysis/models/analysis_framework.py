"""This module contains the analysis framework"""
from django.db import models


class AnalysisFramework(models.Model):
    """Analysis Framework"""
    name = models.CharField(max_length=100)

    class Meta:
        """Table metadata"""
        db_table = 'analysis_framework'
