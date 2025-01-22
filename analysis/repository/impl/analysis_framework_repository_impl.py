"""This module contains the implementation of analysis repository"""
from analysis.contract.to.analysis_framework_to import AnalysisFrameworkTO
from analysis.models.analysis_framework import AnalysisFramework
from analysis.repository.analysis_framework_repository import AnalysisFrameworkRepository
from common.helpers.query_options import QueryOptions


class AnalysisFrameworkRepositoryImpl(AnalysisFrameworkRepository):
    """Implementation of analysis repository"""

    def delete_by_id(self, obj_id):
        """
        Delete analysis framework by id from the database.
        """

    def update(self, obj_id, data):
        """
        Update analysis framework from the database.
        """

    def create(self, data):
        """
        Create analysis framework from the database.
        """

    def get_all(self, query_options: QueryOptions = None, **kwargs):
        """
        Retrieve all analysis frameworks from the database with optional filtering, ordering, and pagination.
        """
        # Build filters dynamically based on provided kwargs
        filters = {key: value for key, value in kwargs.items() if value is not None}

        # Query the database with the filters
        analyses = AnalysisFramework.objects.filter(**filters)

        # If query_options is None, return all results without pagination
        if not analyses.exists():  # Ensure there are results before processing
            return []

        # Transform all results to transfer objects
        return AnalysisFrameworkTO.from_models(analyses)

    def get_by_id(self, obj_id):
        """
        Retrieve a single user by ID.
        """
        try:
            analysis = AnalysisFramework.objects.get(id=obj_id)
            return AnalysisFrameworkTO.from_model(analysis)
        except AnalysisFramework.DoesNotExist:
            return None
