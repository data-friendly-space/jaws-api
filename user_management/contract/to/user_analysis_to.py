'''This module contains the Analysis Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Optional, Dict

from analysis.contract.to.analysis_to import AnalysisTO
from user_management.contract.to.role_to import RoleTO
from user_management.contract.to.user_to import UserTO
from user_management.models.user_analysis_role import UserAnalysisRole


@dataclass
class UserAnalysisTO:
    user: UserTO
    analysis: AnalysisTO
    role: RoleTO

    @classmethod
    def from_model(cls, instance: UserAnalysisRole):
        """Transforms Analysis instance into a AnalysisTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
        return cls(
            user=UserTO.from_model(instance.user),
            analysis=AnalysisTO.from_model(instance.analysis),
            role=RoleTO.from_model(instance.role),
        )

    @classmethod
    def from_models(self, analysis):
        """
        Transform a list of Analysis model instances into a list of AnalysisTO instances.
        """
        return [self.from_model(a) for a in analysis]

    def to_dict(self) -> Dict:
        return asdict(self)
