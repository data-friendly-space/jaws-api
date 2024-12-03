'''This module contains the workspace model'''
from django.db import models

from user_management.models.analysis_framework import AnalysisFramework


class Workspace(models.Model):
    '''Model for the workspace'''
    title = models.CharField(max_length=200)
    creation_date = models.DateTimeField()
    last_access_date = models.DateTimeField()
    facilitator = models.ForeignKey(
        "user_management.User",
        on_delete=models.CASCADE,
        related_name="facilitated_workspaces")
    country = models.CharField(max_length=100)
    analysis_framework = models.ForeignKey(AnalysisFramework, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)
