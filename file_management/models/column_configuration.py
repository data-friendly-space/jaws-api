"""Contains the column configuration model"""
from django.db import models

from analysis.models.analysis import Analysis
from file_management.models.dataset_column import DatasetColumn
from file_management.models.data_role import DataRole
from file_management.models.data_type import DataType

class ColumnConfiguration(models.Model):
    """Dataset Column configuration model"""
    column = models.ForeignKey(DatasetColumn, on_delete=models.CASCADE)
    include = models.BooleanField(default=True)
    alias = models.CharField(max_length=255, null=True, blank=True)
    data_type = models.ForeignKey(DataType, null=True, on_delete=models.SET_NULL)
    data_role = models.ForeignKey(DataRole, null=True, on_delete=models.SET_NULL)
    last_change=models.DateTimeField(auto_now=True)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)

    class Meta:
        """Table's metadata"""
        db_table="column_configurations"
