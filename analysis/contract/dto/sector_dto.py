from analysis.models.sector import Sector


class SectorTO:

    def __init__(
            self,
            id: str,
            name: str
    ):
        self.id = id
        self.name = name

    @classmethod
    def from_model(cls, instance: Sector):
        if instance is None:  # Handle case when instance is None
            return None
        """Transforms Position instance into a PositionTO representation."""
        return cls(
            id=instance.id,
            name=instance.name
        )
    
    @classmethod
    def from_models(cls, sectors):
        if sectors is None or sectors.count() <= 0:
            return None
        return [cls.from_model(sector) for sector in sectors.all()]