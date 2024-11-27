from django.db import models

class Disaggregation(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=100)