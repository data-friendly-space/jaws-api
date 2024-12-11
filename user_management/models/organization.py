"""This module contains the organization model"""
import uuid

from django.db import models


class Organization(models.Model):
    """Organization model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'organization'
