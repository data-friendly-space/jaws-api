from django.db import models


class UiConfiguration(models.Model):
    color = models.CharField(max_length=40)

    def __str__(self):
        return "UI Configuration"
