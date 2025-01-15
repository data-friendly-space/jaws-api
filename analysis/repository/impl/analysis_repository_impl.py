"""This module contains the implementation of analysis repository"""
from typing import List

from analysis.contract.to.administrative_division_to import AdministrativeDivisionTO
from analysis.contract.to.analysis_question_to import AnalysisQuestionTO
from analysis.contract.to.analysis_step_to import AnalysisStepTO
from analysis.contract.to.analysis_to import AnalysisTO
from analysis.contract.to.disaggregation_to import DisaggregationTO
from analysis.contract.to.sector_to import SectorTO
from analysis.models.administrative_division import AdministrativeDivision
from analysis.models.analysis import Analysis
from analysis.models.analysis_question import AnalysisQuestion
from analysis.models.analysis_step import AnalysisStep
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector
from analysis.repository.analysis_repository import AnalysisRepository
from common.contract.to.paginated_to import PaginatedResultTO
from common.helpers.query_options import QueryOptions
from user_management.contract.to.user_analysis_role_to import UserAnalysisRoleTO
from user_management.models.user_analysis_role import UserAnalysisRole


class AnalysisRepositoryImpl(AnalysisRepository):
    """Implementation of analysis repository"""

    def update_analysis_questions(self, analysis_id: int, content: str) -> AnalysisQuestionTO:
        """Assign or update analysis questions"""
        question = AnalysisQuestion.objects.update_or_create(content=content, analysis_id=analysis_id)
        return AnalysisQuestionTO.from_model(question[0]
                                             )

    def assign_or_update_framework_to_analysis(self, analysis_id: int, framework_id: int) -> AnalysisTO:
        """
                Update the analysis_framework field for a specific Analysis instance.

                :param analysis_id: ID of the Analysis to update.
                :param framework_id: ID of the AnalysisFramework to set.
                :return: Number of rows updated.
                """
        # Perform the update query
        Analysis.objects.filter(id=analysis_id).update(analysis_framework=framework_id)
        return AnalysisTO.from_model(Analysis.objects.get(id=analysis_id))

    def get_all(self, query_options: QueryOptions = None, **kwargs):
        """
        Retrieve all analyses from the database with optional filtering, ordering, and pagination.
        """
        # Build filters dynamically based on provided kwargs
        filters = {key: value for key, value in kwargs.items() if value is not None}
        analyses = Analysis.objects.filter(**filters).distinct("id")

        # Ensure query_options exists
        if not query_options:
            query_options = QueryOptions(
                page_number=0,
                page_size=10,
                order_by={"id": "asc"}  # Default ordering by id
            )

        query_options.add_order_by({"id": "asc"})

        # Handle query_options if provided, otherwise return all records without pagination
        if query_options:
            # Get searchable fields, including related fields if needed
            query_options.search_fields = query_options.get_queryable_fields(
                model=Analysis, include_relations=True
            )

            # Apply filters, ordering, and pagination
            analyses = query_options.filter_and_exec_queryset(analyses, model=Analysis)

        return PaginatedResultTO(
            AnalysisTO.from_models(analyses['results']),
            analyses['total']  # Total count with DISTINCT
        )


    def get_by_id(self, obj_id) -> AnalysisTO | None:
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
        Update analysis id.
        """
        try:
            analysis = Analysis.objects.get(id=obj_id)
            disaggregation_ids = [d['id'] for d in disaggregations]  # Extract IDs from disaggregations
            sector_ids = [s['id'] for s in sectors]  # Extract IDs from sectors
            # Set the relationships using the IDs
            analysis.disaggregations.set(disaggregation_ids)  # Assign disaggregations using IDs
            analysis.sectors.set(sector_ids)  # Assign sectors using IDs
            return AnalysisTO.from_model(analysis)
        except Analysis.DoesNotExist:
            return None

    def create(self, data, disaggregations, sectors):
        """
        Add a new analysis to the database.
        """
        # Create the analysis instance

        # Extract only the IDs from disaggregations and sectors
        disaggregation_ids = [d['id'] for d in disaggregations]  # Extract IDs from disaggregations
        sector_ids = [s['id'] for s in sectors]  # Extract IDs from sectors
        analysis = Analysis.objects.create(**data)

        # Set the relationships using the IDs
        analysis.disaggregations.set(disaggregation_ids)  # Assign disaggregations using IDs
        analysis.sectors.set(sector_ids)  # Assign sectors using IDs

        # Return the analysis as a transfer object
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

    def add_location(self, analysis_to: AnalysisTO, location: AdministrativeDivisionTO):
        """Add a new administrative division into a analysis"""
        analysis = Analysis.objects.get(id=analysis_to.id)
        location = AdministrativeDivision.objects.get(p_code=location.pCode)
        analysis.locations.add(location)
        return AdministrativeDivisionTO.from_model(location, include_hierarchy=True)

    def remove_location(self, analysis_to: AnalysisTO, location: AdministrativeDivisionTO):
        """Add a new administrative division into a analysis"""
        analysis = Analysis.objects.get(id=analysis_to.id)
        location = AdministrativeDivision.objects.get(p_code=location.pCode)
        analysis.locations.remove(location)

    def get_steps(self):
        """Return the analysis steps"""
        steps = AnalysisStep.objects.all()
        steps_to = AnalysisStepTO.from_models(steps)
        return steps_to

    def get_steps_by_ids(self, ids):
        """Return analysis steps based on a list of ids"""
        steps = AnalysisStep.objects.filter(id__in=ids)
        steps_to = AnalysisStepTO.from_models(steps)
        return steps_to

    def update_analysis_steps(self, analysis_id: int, step_ids: List[int]):
        """Update the analysis steps"""
        analysis = Analysis.objects.filter(id=analysis_id).first()
        steps = AnalysisStep.objects.filter(id__in=step_ids)
        analysis.analysis_steps.set(steps)

    def invite_user_to_analysis(self, user_id: str, analysis_id: str, role_id: str):
        """Invite user to analysis assigning role"""
        user_analysis_role = UserAnalysisRole.objects.create(analysis_id=analysis_id, role_id=role_id, user_id=user_id)
        return UserAnalysisRoleTO.from_model(user_analysis_role)

    def get_all_sectors(self, **kwargs):
        """
        Retrieve all sectors from the database.
        """
        filters = {key: value for key, value in kwargs.items() if value is not None}
        sectors = Sector.objects.filter(**filters)
        return SectorTO.from_models(sectors)

    def get_all_disaggregations(self, query_options: QueryOptions, **kwargs):
        """
        Retrieve all disaggregations from the database.
        """
        filters = {key: value for key, value in kwargs.items() if value is not None}
        disaggregations = Disaggregation.objects.filter(**filters)
        if query_options:
            disaggregations = query_options.filter_and_exec_queryset(disaggregations, model=Analysis)
        if not disaggregations or len(disaggregations) == 0:
            return []
        return DisaggregationTO.from_models(disaggregations)
