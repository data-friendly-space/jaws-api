"""This module contains the entry model"""
from django.db import models
from django.utils import timezone


class Entry(models.Model):
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
        Creates an Entry instance from an EntryTO instance without saving it.

        Args:
            entry_to (EntryTO): Transfer Object containing the Entry data.

        Returns:
            Entry: An instance of the Entry model.
        """
        from analysis.contract.to.entry_to import EntryTO
        if not isinstance(entry_to, EntryTO):
            raise ValueError("The argument must be an instance of EntryTO")

        # Create the Entry instance without saving
        entry_instance = cls(
            id=entry_to.id,  # Include only if IDs are passed in the TO
        )

        entry_instance.save()

        return entry_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]
