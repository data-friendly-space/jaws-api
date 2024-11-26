from analysis.models.disaggregation import Disaggregation


class DisaggregationTO:

    def __init__(
            self,
            id: str,
            name: str
    ):
        self.id = id
        self.name = name

    @classmethod
    def from_model(cls, instance: Disaggregation):
        if instance is None:  # Handle case when instance is None
            return None
        """Transforms Position instance into a PositionTO representation."""
        return cls(
            id=instance.id,
            name=instance.name
        )
    
    @classmethod
    def from_models(cls, disaggregations):
        if disaggregations is None or disaggregations.count() <= 0:  # Handle case when instance is None
            return None
        return [cls.from_model(disaggregation) for disaggregation in disaggregations.all()]
