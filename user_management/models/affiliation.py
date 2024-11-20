from django.db import models


class Affiliation(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, blank=True, null=True)
    background = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
