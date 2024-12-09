"""This module contains the role model"""
from django.db import models


class Role(models.Model):
    """Role model"""
    role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.role)

    class Meta:
        db_table = 'role'
