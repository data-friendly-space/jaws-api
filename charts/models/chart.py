"""This module contains the chart model"""

from django.db import models

from analysis.models.analysis import Analysis
from file_management.models.column_configuration import ColumnConfiguration
from file_management.models.dataset import Dataset


class Chart(models.Model):
    """Model for charts"""

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    x_col = models.ForeignKey(ColumnConfiguration, on_delete=models.CASCADE, related_name="x_col")
    y_cols = models.ManyToManyField(ColumnConfiguration, related_name="y_cols")
    title = models.CharField(max_length=255, null=True)
    x_label = models.CharField(max_length=255, null=True)
    y_label = models.CharField(max_length=255, null=True)
    type = models.CharField(
        choices=[("bar", "Bar"), ("line", "Line"), ("pie", "Pie")], default="bar"
    )
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)

    class Meta:
        """Table's metadata"""
        db_table="chart"
