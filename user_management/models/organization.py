'''This module contains the organization model'''
from django.db import models


class Organization(models.Model):
    '''Organization model'''
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'organization'
