"""This module contains the model for a dataset's column"""
from django.db import models


class DatasetColumn(models.Model):
    """Dataset column model"""
    dataset = models.ForeignKey('file_management.Dataset', on_delete=models.CASCADE)
    original_name = models.CharField(max_length=255)
    original_data_type = models.ForeignKey('file_management.DataType', null=True, on_delete=models.SET_NULL)

    class Meta:
        """Table's metadata"""
        db_table="dataset_column"
        constraints = [
            models.UniqueConstraint(
                fields=[ "dataset", "original_name"],
                name="unique_col_per_dataset"
            )
        ]
