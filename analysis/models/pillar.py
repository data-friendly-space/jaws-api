"""This module contains the pillar model"""
from django.db import models

from analysis.models.sub_pillar import SubPillar


class Pillar(models.Model):
    """Sector model"""
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=200,null=True)
    sub_pillars = models.ManyToManyField(SubPillar)
    class Meta:
        """Table's metadata"""
        db_table = 'pillar'
