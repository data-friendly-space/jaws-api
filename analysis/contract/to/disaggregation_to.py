"""This module contains the disaggregation Transfer Object"""
from dataclasses import dataclass

from analysis.models.disaggregation import Disaggregation
from common.contract.to.base_to import BaseTO


@dataclass
class DisaggregationTO(BaseTO):
    """Disaggregation TO"""
    id: str
    name: str
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
