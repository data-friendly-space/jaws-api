'''This module contains the affiliation model'''
from django.db import models


class Affiliation(models.Model):
    '''Affiliation model'''
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, blank=True, null=True)
    background = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'affiliation'
