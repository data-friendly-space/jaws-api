from rest_framework import serializers

from user_management.models import Organization


class OrganizationTO(serializers.ModelSerializer):
    def __init__(
            self,
            id: int,
            name: str
    ):
        self.id = id
        self.name = name

    @classmethod
    def from_model(cls, instance: Organization):
        if instance is None:  # Handle case when instance is None
            return None
        """Transforms Organization instance into a OrganizationTO representation."""
        return cls(
            id=instance.id,
            name=instance.name,
        )
