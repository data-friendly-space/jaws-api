from user_management.models import Role, UiConfiguration


class UiConfigurationTO:
    def __init__(
            self,
            id: int,
            color: str
    ):
        self.id = id
        self.color = color

    @classmethod
    def from_model(cls, instance: UiConfiguration):
        if instance is None:  # Handle case when instance is None
            return None
        """Transforms UiConfiguration instance into a UiConfigurationTO representation."""
        return cls(
            id=instance.id,
            color=instance.color,
        )
