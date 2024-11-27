from django.db import models

class Sector(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=100)