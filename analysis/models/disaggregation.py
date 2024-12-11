"""Contains the disaggregation model"""
from django.db import models


class Disaggregation(models.Model):
    """Disaggregation model"""
    name = models.CharField(max_length=100)

    class Meta:
        """Table's metadata"""
        db_table = 'disaggregation'
