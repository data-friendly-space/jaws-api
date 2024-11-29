'''This module contains the permission model'''
from django.db import models

from user_management.models import Role


class Permission(models.Model):
    '''Permission model'''
    name = models.CharField(max_length=50, unique=True)
    TYPE_CHOICES = [
        ('read', 'Read'),
        ('write', 'Write'),
        ('all', 'All'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.type})"


Role.permissions = models.ManyToManyField(Permission)
