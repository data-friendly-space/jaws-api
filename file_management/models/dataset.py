"""Contains the dataset model"""
import uuid
from django.db import models

class Dataset(models.Model):
    """Dataset model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    filename = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE)
    mime_type = models.CharField(null=False, default="text/csv")
    size_bytes = models.IntegerField()
    total_rows = models.IntegerField()
    total_columns = models.IntegerField()

    class Meta:
        """Table's metadata"""
        db_table = 'dataset'
        ordering = ['created_at']
