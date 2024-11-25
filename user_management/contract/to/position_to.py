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
        if instance is None:  # Handle case when instance is None
            return None
        """Transforms Position instance into a PositionTO representation."""
        return cls(
            id=instance.id,
            name=instance.name
        )
