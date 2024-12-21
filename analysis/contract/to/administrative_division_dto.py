"""This module contains the analysis DTO"""

from dataclasses import asdict, dataclass
from analysis.models.administrative_division import AdministrativeDivision
from common.contract.to.base_to import BaseTO

@dataclass
class AdministrativeDivisionTO(BaseTO):
    """Administrative Division Data Transfer Object"""

    def __init__(self, p_code: str, name: str, hierarchy=None):
        self.pCode = p_code
        self.name = name
        self.hierarchy = hierarchy

    @classmethod
    def from_model(cls, instance: AdministrativeDivision, include_hierarchy=False):
        """Transforms Analysis instance into a AnalysisDTO representation."""
        if instance is None:
            return None
        if not include_hierarchy:
            return cls(
                p_code=instance.p_code,
                name=instance.name,
            )
        hierarchy = instance.get_hierarchy()
        hierarchy_data = [
            {"pCode": loc.p_code, "name": loc.name, "adminLevel": loc.admin_level}
            for loc in hierarchy
        ]
        return cls(p_code=instance.p_code, name=instance.name, hierarchy=hierarchy_data)

    @classmethod
    def from_models(cls, administrative_divisions, include_hierarchy=False):
        """
        Transform a list of Administrative Division model into a list of AdministrativeDivisionTO.
        """
        if administrative_divisions is None or administrative_divisions.count() <= 0:
            return None
        return [
            cls.from_model(administrative_division, include_hierarchy)
            for administrative_division in administrative_divisions.all()
        ]

    def to_dict(self):
        return self.__dict__
