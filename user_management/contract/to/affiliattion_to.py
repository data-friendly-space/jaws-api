from user_management.models import Affiliation


class AffiliationTO:
    def __init__(
            self,
            id: int,
            name: str
    ):
        self.id = id
        self.name = name

    @classmethod
    def from_model(cls, instance: Affiliation):
        if instance is None:  # Handle case when instance is None
            return None
        """Transforms Affiliation instance into a AffiliationTO representation."""
        return cls(
            id=instance.id,
            name=instance.name,
        )
