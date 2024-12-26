"""This module contains the analysis step Transfer Object"""
from dataclasses import dataclass

from analysis.models.analysis_step import AnalysisStep
from common.contract.to.base_to import BaseTO


@dataclass
class AnalysisStepTO(BaseTO):
    """Analysis Step TO"""
    id: int
    name: str
    order: int
    mandatory: bool
    parentStepId: int

    @classmethod
    def from_model(cls, instance: AnalysisStep):
        """Transforms analysis step model to analyisis step transfer object representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            name=instance.name,
            order=instance.order,
            mandatory=instance.mandatory,
            parentStepId=instance.step_parent.id if instance.step_parent else None
        )

    @classmethod
    def from_models(cls, steps):
        """Create multiple analysis step to based on analysis step model"""
        if steps is None or steps.count() <= 0:
            return None
        return [cls.from_model(step) for step in steps.all()]
