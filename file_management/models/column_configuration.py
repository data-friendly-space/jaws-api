"""Contains the column configuration model"""
from django.db import models

from file_management.models.data_role import DataRole
from file_management.models.data_type import DataType
from file_management.models.dataset import Dataset

class ColumnConfiguration(models.Model):
    """Dataset Column configuration model"""

    dataset = models.ForeignKey(
        Dataset,
        primary_key=True,
        on_delete=models.CASCADE)
    original_name = models.CharField(
        primary_key=True,
        max_length=255
    )
    include = models.BooleanField(default=True)
    alias = models.CharField(max_length=255, null=True, blank=True)
    data_type = models.ForeignKey(DataType, null=True, on_delete=models.SET_NULL)
    data_role = models.ForeignKey(DataRole, null=True, on_delete=models.SET_NULL)
    last_change=models.DateTimeField(auto_now=True)

    class Meta:
        """Table's metadata"""
        db_table="column_configurations"
