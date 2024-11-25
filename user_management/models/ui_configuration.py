from django.db import models


class UiConfiguration(models.Model):
    color = models.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.name = None

    def __str__(self):
        return "UI Configuration"
