"""This module contains the position module"""
from django.db import models

class Position(models.Model):
    """Position module"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'position'
