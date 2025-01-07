'''This module contains the Analysis Transfer Object'''
from dataclasses import asdict, dataclass

from analysis.models.analysis_question import AnalysisQuestion
from common.contract.to.base_to import BaseTO


@dataclass
class AnalysisQuestionTO(BaseTO):
    '''AnalysisQuestion Transfer Object'''
    id: int
    content: str


    @classmethod
    def from_model(cls, instance: AnalysisQuestion):
        """Transforms AnalysisQuestion instance into a AnalysisQuestionTO representation."""
        if instance is None:
            return None
        return cls(
            id=instance.id,
            content=instance.content,

        )
