"""Contains the disaggregation model"""
from django.db import models, transaction

from common.models import BaseModel


class Disaggregation(models.Model, BaseModel):
    """Disaggregation model"""
    name = models.CharField(max_length=100)

    class Meta:
        """Table's metadata"""
        db_table = 'disaggregation'

    @classmethod
    def from_to(cls, disaggregation_to):
        """
        Creates an Disaggregation instance from an DisaggregationTO instance without saving it.

        Args:
            disaggregation_to (DisaggregationTO): Transfer Object containing the Disaggregation data.

        Returns:
            Disaggregation: An instance of the Disaggregation model.
        """
        from analysis.contract.to.disaggregation_to import DisaggregationTO

        if disaggregation_to is None:
            return None

        if not isinstance(disaggregation_to, DisaggregationTO):
            raise ValueError("The argument must be an instance of DisaggregationTO")

        with transaction.atomic():
            # Create the Disaggregation instance without saving
            disaggregation_instance = cls(
                id=disaggregation_to.id,  # Include only if IDs are passed in the TO
                name=disaggregation_to.name,
            )

        return disaggregation_instance
