"""This module contains the entry model"""
from django.db import models, transaction
from django.utils import timezone

from analysis.models.sub_pillar import SubPillar
from common.models import BaseModel


class Entry(models.Model,BaseModel):
    """Entry model"""
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255)
    fragment = models.CharField(max_length=600)
    source = models.CharField(max_length=255)
    tag = models.ForeignKey('analysis.SubPillar', related_name='entries', on_delete=models.CASCADE)

    class Meta:
        """Table's metadata"""
        db_table = 'entry'

    @classmethod
    def from_to(cls, entry_to):
        """
        Creates or updates an Entry instance from an EntryTO instance.

        Args:
            entry_to (EntryTO): Transfer Object containing the Entry data.

        Returns:
            Entry: An instance of the Entry model.
        """
        from analysis.contract.to.entry_to import EntryTO
        from analysis.models.sub_pillar import SubPillar

        if not isinstance(entry_to, EntryTO):
            raise ValueError("The argument must be an instance of EntryTO")

        # Resolve ForeignKey relationship for 'tag'
        tag_instance = SubPillar.from_to(entry_to.tag) if entry_to.tag else None

        # Build the defaults dictionary
        defaults = {
            "created_at": entry_to.createdAt,
            "created_by": entry_to.createdBy,
            "fragment": entry_to.fragment,
            "source": entry_to.source,
            "tag": tag_instance,
        }

        # Filter out None values to avoid overwriting existing data
        defaults = {key: value for key, value in defaults.items() if value is not None}

        with transaction.atomic():
            # Update or create the Entry instance
            entry_instance, created = cls.objects.update_or_create(
                id=entry_to.id,  # Match by ID if provided
                defaults=defaults,
            )

        return entry_instance

