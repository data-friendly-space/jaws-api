"""Contains the analysis step model"""
from django.db import models

class AnalysisStep(models.Model):
    """Contains the model for an step within an analysis"""

    step_parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        default=None,
        null=True)
    order = models.IntegerField()
    name = models.CharField(blank=False)
    mandatory = models.BooleanField(default=True)


    class Meta:
        """Table metadata"""
        db_table = "analysis_step"
        verbose_name = "Analysis Step"
        verbose_name_plural = "Analyisis Steps"

    def __str__(self):
        """Return the analysis step as string"""
        return str(self.name)
