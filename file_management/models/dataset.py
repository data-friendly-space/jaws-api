"""Contains the dataset model"""
import uuid
from django.db import models

class Dataset(models.Model):
    """Dataset model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    filename = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE)
    mime_type = models.CharField(null=False, default="text/csv")
    size_bytes = models.IntegerField()
    total_rows = models.IntegerField()
    total_columns = models.IntegerField()
    external_identifier = models.CharField()
    class Meta:
        """Table's metadata"""
        db_table = 'dataset'
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(
                fields=[ "filename", "url"],
                name="unique_filename_url"
            )
        ]


    def create_new_version(self, size_bytes: int, total_columns: int, total_rows: int) -> 'Dataset':
        """Create a new version of the dataset"""
        new_dataset = Dataset(
            filename=self.filename,
            url=self.url,
            created_at=self.created_at,
            mime_type=self.mime_type,
            size_bytes=size_bytes,
            total_columns=total_columns,
            total_rows=total_rows
        )
        return new_dataset
