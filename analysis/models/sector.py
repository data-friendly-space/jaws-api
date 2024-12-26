"""This module contains the sector model"""
from django.db import models


class Sector(models.Model):
    """Sector model"""
    name = models.CharField(max_length=100)

    class Meta:
        """Table's metadata"""
        db_table = 'sector'
