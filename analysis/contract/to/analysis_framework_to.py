"""This module contains the Analysis Transfer Object"""
from dataclasses import dataclass

from analysis.contract.to.pillar_to import PillarTO
from analysis.models.analysis_framework import AnalysisFramework
from common.contract.to.base_to import BaseTO


@dataclass
class AnalysisFrameworkTO(BaseTO):
    """Analysis Framework Transfer Object"""
    id: int
    name: str
    pillars: list[PillarTO]
    model_class = AnalysisFramework

    @classmethod
    def from_model(cls, instance: AnalysisFramework) -> 'AnalysisFrameworkTO':
        """Transforms Analysis instance into a AnalysisFrameworkTO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            name=instance.name,
            pillars=PillarTO.from_models(instance.pillars.all())
        )
