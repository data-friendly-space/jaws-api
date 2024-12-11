"""This module contains the workspace model"""
import uuid

from django.db import models


class Workspace(models.Model):
    """Model for the workspace"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_access_date = models.DateTimeField(null=True)
    facilitator = models.ForeignKey("user_management.User", on_delete=models.CASCADE,
                                    related_name="facilitated_workspaces")
    country = models.CharField(max_length=100)
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="organizations",
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'workspace'
