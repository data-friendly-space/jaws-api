"""This module contains the theme model"""
from django.db import models


class Theme(models.Model):
    """Theme model"""
    id = models.CharField(primary_key=True, max_length=36)
    logo_url = models.URLField()
    color = models.CharField(max_length=6)

    class Meta:
        db_table = 'theme'
