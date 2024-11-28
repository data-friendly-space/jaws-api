'''This module contains the ui configuration model'''
from django.db import models


class UiConfiguration(models.Model):
    '''Ui configuration module'''
    color = models.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.name = None

    def __str__(self):
        return "UI Configuration"
