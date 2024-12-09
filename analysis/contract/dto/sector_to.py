'''This module contains the disaggregation Transfer Object'''
from analysis.models.sector import Sector


class SectorTO:
    '''Sector DTO'''
    def __init__(
            self,
            id: str,
            name: str
    ):
        self.id = id
        self.name = name

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
        '''Creatre a sector TO based on a database model'''
        if sectors is None or sectors.count() <= 0:
            return None
        return [cls.from_model(sector) for sector in sectors.all()]
