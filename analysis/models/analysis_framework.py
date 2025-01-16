"""This module contains the analysis framework"""
from django.db import models

from analysis.models.pillar import Pillar


class AnalysisFramework(models.Model):
    """Analysis Framework"""
    name = models.CharField(max_length=100)
    pillars = models.ManyToManyField(Pillar)


    class Meta:
        """Table metadata"""
        db_table = 'analysis_framework'
