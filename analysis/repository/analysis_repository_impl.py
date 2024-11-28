'''This module contains the implementation of analysis repository'''
from analysis.contract.dto.analysis_dto import AnalysisTO
from analysis.contract.repository.analysis_repository import AnalysisRepository
from analysis.models.analysis import Analysis

class AnalysisRepositoryImpl(AnalysisRepository):
    '''Implementation of analysis repository'''
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
