"""This module contains the entry model"""


from common.models.base_model import BaseModel


class Entry(BaseModel):
    """Entry model"""

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
