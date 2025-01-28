"""Contains the dataset model"""
import uuid

from django.db import models, transaction

from common.models import BaseModel


class Dataset(models.Model, BaseModel):
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
                fields=["filename", "url"],
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

    @classmethod
    def from_to(cls, dataset_to):
        """
        Creates or updates a Dataset instance from a DatasetTO instance.

        Args:
            dataset_to (DatasetTO): Transfer Object containing the Dataset data.

        Returns:
            Dataset: An instance of the Dataset model.
        """
        from file_management.contract.dto.dataset_to import DatasetTO
        from user_management.models import User

        if dataset_to is None:
            return None

        if not isinstance(dataset_to, DatasetTO):
            raise ValueError("The argument must be an instance of DatasetTO")

        # Resolve ForeignKey relationship for uploaded_by
        uploaded_by_instance = (
            User.objects.get(id=dataset_to.uploadedBy)
            if dataset_to.uploadedBy
            else None
        )

        # Build the defaults dictionary
        defaults = {
            "filename": dataset_to.filename,
            "url": dataset_to.url,
            "mime_type": dataset_to.mimeType,
            "size_bytes": dataset_to.sizeBytes,
            "total_rows": dataset_to.totalRows,
            "total_columns": dataset_to.totalColumns,
            "external_identifier": dataset_to.externalIdentifier,
            "uploaded_by": uploaded_by_instance,
        }

        # Filter out None values to avoid overwriting
        defaults = {key: value for key, value in defaults.items() if value is not None}

        with transaction.atomic():
            # Update or create the Dataset instance
            dataset_instance, created = cls.objects.update_or_create(
                id=dataset_to.id,  # Match by ID if provided
                defaults=defaults,
            )

        return dataset_instance

