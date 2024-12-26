"""Contains the dataset model"""
from django.db import models

class Dataset(models.Model):
    """Dataset model"""

    dataset_reference = models.CharField(max_length=255)
    dataset_url = models.URLField(null=True)

    class Meta:
        """Table's metadata"""
        db_table = 'dataset'
