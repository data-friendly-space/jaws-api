"""This module contains the disaggregation Transfer Object"""
from analysis.models.disaggregation import Disaggregation


class DisaggregationTO:
    """Disaggregation TO"""
    def __init__(
            self,
            id: str,
            name: str
    ):
        self.id = id
        self.name = name

    @classmethod
    def from_model(cls, instance: Disaggregation):
        """Transforms Position instance into a DisaggregationTO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            name=instance.name
        )

    @classmethod
    def from_models(cls, disaggregations):
        """Create a disaggregation to based on a database model"""
        if disaggregations is None or disaggregations.count() <= 0:
            return None
        return [cls.from_model(disaggregation) for disaggregation in disaggregations.all()]