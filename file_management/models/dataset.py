"""Contains the dataset model"""
import uuid
from django.db import models

class Dataset(models.Model):
    """Dataset model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    filename = models.CharField(max_length=255)
    url = models.URLField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE)

    class Meta:
        """Table's metadata"""
        db_table = 'dataset'
        ordering = ['created_on']
