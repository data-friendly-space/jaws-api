"""This module contains the analysis question"""
from django.db import models



class AnalysisQuestion(models.Model):
    """Analysis Question"""
    content = models.CharField(max_length=240)
    analysis = models.ForeignKey('analysis.Analysis', on_delete=models.CASCADE, related_name='analysis_questions')

    class Meta:
        """Table metadata"""
        db_table = 'analysis_question'
