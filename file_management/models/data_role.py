"""Contains the data role model"""
from django.db import models

class DataRole(models.Model):
    """Dataset Data Role model"""
    name=models.CharField(max_length=255)

    class Meta:
        """Table's metadata"""
        db_table="data_roles"
