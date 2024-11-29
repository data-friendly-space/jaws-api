'''This module contains the analysis framework model'''
from django.db import models


class AnalysisFramework(models.Model):
    '''Analysis framework model'''
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)
