"""This module contains the sub_pillar model"""
from django.db import models


class SubPillar(models.Model):
    """Sector model"""
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=200,null=True)

    class Meta:
        """Table's metadata"""
        db_table = 'sub_pillar'
