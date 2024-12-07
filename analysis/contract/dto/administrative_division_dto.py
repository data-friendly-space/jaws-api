'''This module contains the analysis DTO'''
from analysis.models.administrative_division import AdministrativeDivision


class AdministrativeDivisionTO:
    '''Administrative Division Data Transfer Object'''
    def __init__(
            self,
            p_code: str,
            name: str
    ):
        self.p_code = p_code
        self.name = name

    @classmethod
    def from_model(cls, instance: AdministrativeDivision):
        """Transforms Analysis instance into a AnalysisDTO representation."""
        if instance is None:
            return None
        return cls(
            p_code=instance.p_code,
            name=instance.name,
        )

    @classmethod
    def from_models(cls, analyses):
        """
        Transform a list of Administrative Division model into a list of AdministrativeDivisionTO.
        """
        return [cls.from_model(analysis) for analysis in analyses]
