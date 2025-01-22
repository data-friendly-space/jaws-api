"""This module contains the analysis framework"""
from django.db import models


from analysis.models.pillar import Pillar
from common.models.base_model import BaseModel


class AnalysisFramework(BaseModel):
    """Analysis Framework"""

    name = models.CharField(max_length=100)
    pillars = models.ManyToManyField(Pillar)

    class Meta:
        """Table metadata"""
        db_table = 'analysis_framework'

    @classmethod
    def from_to(cls, analysis_framework_to):
        """
        Creates an AnalysisFramework instance from an AnalysisFrameworkTO instance without saving it.

        Args:
            analysis_framework_to (AnalysisFrameworkTO): Transfer Object containing the AnalysisFramework data.

        Returns:
            AnalysisFramework: An instance of the AnalysisFramework model.
        """
        from analysis.contract.to.analysis_framework_to import AnalysisFrameworkTO
        if not isinstance(analysis_framework_to, AnalysisFrameworkTO):
            raise ValueError("The argument must be an instance of AnalysisFrameworkTO")

        # Create the AnalysisFramework instance without saving
        analysis_framework_instance = cls(
            id=analysis_framework_to.id,  # Include only if IDs are passed in the TO
            name=analysis_framework_to.name,
            pillars= Pillar.from_tos(analysis_framework_to.pillars)
        )

        return analysis_framework_instance
