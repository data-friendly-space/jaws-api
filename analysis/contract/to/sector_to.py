"""This module contains the disaggregation Transfer Object"""
from dataclasses import dataclass

from analysis.models.sector import Sector
from common.contract.to.base_to import BaseTO


@dataclass
class SectorTO(BaseTO):
    """Sector DTO"""
    id: str
    name: str

    @classmethod
    def from_model(cls, instance: Sector):
        """Transforms Sector instance into a Sector TO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            name=instance.name
        )

    @classmethod
    def from_models(cls, sectors):
        """Creatre a sector TO based on a database model"""
        if sectors is None or sectors.count() <= 0:
            return None
        return [cls.from_model(sector) for sector in sectors.all()]
