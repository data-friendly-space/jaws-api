"""This module contains the implementation of analysis repository"""
from analysis.contract.to.analysis_to import AnalysisTO
from analysis.contract.to.administrative_division_dto import AdministrativeDivisionTO
from analysis.contract.repository.analysis_repository import AnalysisRepository
from analysis.models.administrative_division import AdministrativeDivision
from analysis.models.analysis import Analysis


class AnalysisRepositoryImpl(AnalysisRepository):
    """Implementation of analysis repository"""

    def get_all(self):
        """
        Retrieve all users from the database.
        """
        analyses = Analysis.objects.all()
        if not analyses or len(analyses) == 0:
            return []
        return AnalysisTO.from_models(analyses)

    def get_by_id(self, obj_id):
        """
        Retrieve a single user by ID.
        """
        try:
            analysis = Analysis.objects.get(id=obj_id)
            return AnalysisTO.from_model(analysis)
        except Analysis.DoesNotExist:
            return None

    def delete_by_id(self, obj_id):
        """
        Delete a user by ID.
        """
        try:
            analysis = Analysis.objects.get(id=obj_id)
            analysis.delete()
            return True
        except Analysis.DoesNotExist:
            return False

    def update(self, obj_id, data, sectors, disaggregations):
        """
        Update a user by ID.
        """
        try:
            analysis = Analysis.objects.get(id=obj_id)
            for field, value in data.items():
                if field == "sectors":
                    analysis.sectors.set(sectors)
                elif field == "disaggregations":
                    analysis.disaggregations.set(disaggregations)
                else:
                    setattr(analysis, field, value)
            analysis.save()
            return AnalysisTO.from_model(analysis)
        except Analysis.DoesNotExist:
            return None

    def create(self, data, disaggregations, sectors):
        """
        Add a new analysis to the database.
        """
        analysis = Analysis.objects.create(**data)
        analysis.disaggregations.set(disaggregations)
        analysis.sectors.set(sectors)
        return AnalysisTO.from_model(analysis)

    def get_administrative_divisions(self, parent_p_code):
        """
        Retrieves every administrative division within the parent p_code.
        If parent p_code is None, retrieve all the level 0 administrative divisions
        """
        administrative_divisions = None
        if not parent_p_code:
            administrative_divisions = AdministrativeDivision.objects.filter(admin_level=0).all()
        else:
            administrative_divisions = AdministrativeDivision.objects.filter(parent_p_code=parent_p_code).all()
        return AdministrativeDivisionTO.from_models(administrative_divisions)

    def get_administrative_division(self, p_code):
        """Retrieves a specific administrative division by id"""
        administrative_division = AdministrativeDivision.objects.filter(p_code=p_code).first()
        return AdministrativeDivisionTO.from_model(administrative_division, include_hierarchy=True)

    def add_location(self, analysis: Analysis, administrative_division: AdministrativeDivision):
        """Add a new administrative division into a analysis"""
        analysis.locations.add(administrative_division)
        return AdministrativeDivisionTO.from_model(administrative_division, include_hierarchy=True)

    def remove_location(self, analysis: Analysis, administrative_division: AdministrativeDivision):
        """Add a new administrative division into a analysis"""
        analysis.locations.remove(administrative_division)
