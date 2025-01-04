"""This module contains the implementation of analysis repository"""
from analysis.contract.to.analysis_to import AnalysisTO
from analysis.repository.analysis_framework_repository import AnalysisFrameworkRepository
from analysis.contract.to.analysis_framework_to import AnalysisFrameworkTO
from analysis.models.analysis import AnalysisFramework, Analysis
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

    def get_all(self, query_options: QueryOptions, **kwargs):
        """
        Retrieve all analysis from the database.
        """
        filters = {key: value for key, value in kwargs.items() if value is not None}
        analyses = AnalysisFramework.objects.filter(**filters)
        if query_options:
            analyses = query_options.filter_and_exec_queryset(analyses, model=AnalysisFramework)
        if not analyses or len(analyses) == 0:
            return []
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
