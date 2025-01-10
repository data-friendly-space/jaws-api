"""Contains the data type model"""
from django.db import models

class DataType(models.Model):
    """Dataset Data Type model"""
    name=models.CharField(max_length=255)

    class Meta:
        """Table's metadata"""
        db_table="data_types"
