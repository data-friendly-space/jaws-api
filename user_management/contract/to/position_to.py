'''This module contains the Position Transfer Object'''
from user_management.models import Position


class PositionTO:

    def __init__(
            self,
            id: int,
            name: str
    ):
        self.id = id
        self.name = name

    @classmethod
    def from_model(cls, instance: Position):
        """Transforms Position instance into a PositionTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            id=instance.id,
            name=instance.name
        )
