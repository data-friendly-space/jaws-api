"""This module contains the chart model"""

from django.db import models

from analysis.models.analysis import Analysis
from analysis.models.sub_pillar import SubPillar
from charts.contract.dto.chart_to import ChartTO
from common.models.base_model import BaseModel
from file_management.models.column_configuration import ColumnConfiguration
from file_management.models.dataset import Dataset
from user_management.models.user import User


class Chart(BaseModel,models.Model):
    """Model for charts"""


    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    x_col = models.ForeignKey(ColumnConfiguration, on_delete=models.CASCADE, related_name="x_col")
    y_cols = models.ManyToManyField(ColumnConfiguration, related_name="y_cols")
    title = models.CharField(max_length=255, null=True)
    x_label = models.CharField(max_length=255, null=True)
    y_label = models.CharField(max_length=255, null=True)
    subpillar = models.ForeignKey(SubPillar, null=True, on_delete=models.SET_NULL)
    type = models.CharField(
        choices=[("bar", "Bar"), ("line", "Line"), ("pie", "Pie")], default="bar"
    )
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)

    class Meta:
        """Table's metadata"""
        db_table="chart"

    def from_to(cls, instance):
        pass
