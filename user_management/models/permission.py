"""This module contains the permission model"""
from django.db import models


class Permission(models.Model):
    """Permission model"""
    name = models.CharField(max_length=65, unique=True)
    alias = models.CharField(max_length=65, unique=True)
    TYPE_CHOICES = [
        ('read', 'Read'),
        ('write', 'Write'),
        ('all', 'All'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        db_table = 'permission'
