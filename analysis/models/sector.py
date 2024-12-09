"""This module contains the sector model"""
from django.db import models


class Sector(models.Model):
    """Sector model"""
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=100)


    class Meta:
        db_table = 'sector'
