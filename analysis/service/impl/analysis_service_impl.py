"""Contains the implementation of AnalysisService"""

from typing import List
from analysis.contract.io.create_analysis_in import CreateAnalysisIn
from analysis.contract.io.update_analysis_in import UpdateAnalysisIn
from analysis.contract.to import administrative_division_to
from analysis.interfaces.serializers.administrative_division_serializer import (
    AdministrativeDivisionSerializer,
)
from analysis.models.administrative_division import AdministrativeDivision
from analysis.models.analysis import Analysis
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector
from analysis.repository.impl.analysis_framework_repository_impl import AnalysisFrameworkRepositoryImpl
from analysis.repository.impl.analysis_repository_impl import AnalysisRepositoryImpl
from analysis.service.analysis_service import AnalysisService
from analysis.use_cases.add_location_uc import AddLocationUC
from analysis.use_cases.assign_or_update_analysis_framework_uc import AssignOrUpdateAnalysisFrameworkUC
from analysis.use_cases.create_analysis_uc import CreateAnalysisUC
from analysis.use_cases.create_or_update_analysis_question_uc import CreateOrUpdateAnalysisQuestionUC
from analysis.use_cases.get_administrative_division_by_pcode_uc import GetAdministrativeDivisionByPCodeUC
from analysis.use_cases.get_administrative_divisions_uc import GetAdministrativeDivisionsUC, \
    GetAdministrativeDivisionByIdUC
from analysis.use_cases.get_all_disaggregations_uc import GetAllDisaggregationsUC
from analysis.use_cases.get_all_sectors_uc import GetAllSectorsUC
from analysis.use_cases.get_analysis_by_id_uc import GetAnalysisByIdUC
from analysis.use_cases.get_analyses_uc import GetAnalysesUC
from analysis.use_cases.get_analysis_frameworks_uc import GetAnalysisFrameworkUC
from analysis.use_cases.get_steps_uc import GetStepsUC
from analysis.use_cases.put_analysis_scope_uc import PutAnalysisScopeUC
from analysis.use_cases.remove_location_uc import RemoveLocationUC
from analysis.use_cases.update_analysis_steps_uc import UpdateAnalysisStepsUC
from common.exceptions.exceptions import BadRequestException, NotFoundException
from common.helpers.query_options import QueryOptions
from user_management.repository.impl.user_repository_impl import UserRepositoryImpl
from user_management.usecases.get_user_uc_by_filters_uc import GetUserByFiltersUC


class AnalysisServiceImpl(AnalysisService):
    """Implementation of AnalysisService. Contains the business logic"""

    def __init__(self):
        self.create_analysis_uc = CreateAnalysisUC.get_instance()
        self.put_analysis_scope_uc = PutAnalysisScopeUC.get_instance()
        self.get_analysis_uc = GetAnalysesUC.get_instance()
        self.get_analysis_by_id_uc = GetAnalysisByIdUC.get_instance()
        self.get_administrative_divisions_uc = GetAdministrativeDivisionsUC.get_instance()
        self.get_administrative_division_by_code_uc = GetAdministrativeDivisionByPCodeUC.get_instance()
        self.get_administrative_division_by_id_uc = (
            GetAdministrativeDivisionByIdUC.get_instance()
        )
        self.add_location_uc = AddLocationUC.get_instance()
        self.remove_location_uc = RemoveLocationUC.get_instance()
        self.get_user_by_filter_uc = GetUserByFiltersUC.get_instance()
        self.get_steps_uc = GetStepsUC.get_instance()
        self.update_analysis_steps_uc = UpdateAnalysisStepsUC.get_instance()
        self.repository = AnalysisRepositoryImpl()
        self.user_repository = UserRepositoryImpl()
        self.get_all_analysis_frameworks_uc = GetAnalysisFrameworkUC.get_instance()
        self.get_all_sectors_uc = GetAllSectorsUC.get_instance()
        self.assign_or_update_analysis_framework_uc = AssignOrUpdateAnalysisFrameworkUC.get_instance()
        self.create_or_update_analysis_question_uc = CreateOrUpdateAnalysisQuestionUC.get_instance()
        self.get_all_disaggregations_uc = GetAllDisaggregationsUC.get_instance()

    def get_all_analysis_frameworks(self, query_options: QueryOptions):
        """Get all analysis frameworks"""
        analysis_frameworks = self.get_all_analysis_frameworks_uc.exec(AnalysisFrameworkRepositoryImpl(), query_options)
        return [analysis_framework.to_dict() for analysis_framework in analysis_frameworks]

    def update_analysis_framework(self, analysis_id: int, analysis_framework_id: int):
        """ Updates analysis framework"""
        analysis = self.assign_or_update_analysis_framework_uc.exec(self.repository, analysis_id,
                                                                    analysis_framework_id)
        return analysis.to_dict()

    def update_analysis_questions(self, analysis_id: int, content: str):
        """Update analysis questions"""
        analysis_question = self.create_or_update_analysis_question_uc.exec(self.repository, analysis_id, content)
        return analysis_question.to_dict()

    def get_all_sectors(self, **kwargs):
        """Get all sectors"""
        sectors = self.get_all_sectors_uc.exec(AnalysisRepositoryImpl(), **kwargs)
        return [sector.to_dict() for sector in sectors]

    def create_analysis(self, analysis: CreateAnalysisIn, creator_id):
        """Create analysis business logic"""
        if not self.get_user_by_filter_uc.exec(self.user_repository, id=creator_id):
            raise BadRequestException("Analysis creator doens't exists")
        if not analysis.is_valid():
            raise BadRequestException(
                "Create analysis request is not valid: ",
                analysis.errors)
        scope = analysis.validated_data
        if scope['disaggregations']:
            disaggregations = self.get_all_disaggregations_uc.exec(AnalysisRepositoryImpl(), None,
                                                                   pk__in=scope['disaggregations'])
        else:
            disaggregations = []
        sectors = self.get_all_sectors_uc.exec(self.repository, pk__in=scope['sectors'])
        self.validate_scope_fields(scope, sectors)
        data = {
            "title": scope["title"],
            "objectives": scope["objectives"],
            "start_date": scope["start_date"],
            "end_date": scope["end_date"],
            "creator_id": creator_id,
            "workspace_id": scope['workspace_id'],
        }
        new_analysis = self.create_analysis_uc.exec(
            self.repository, data, disaggregations, sectors
        )
        return new_analysis.to_dict()

    def put_analysis_scope(self, analysis: UpdateAnalysisIn, analysis_id, user_id):
        self.get_analysis_by_id(analysis_id)

        # TODO: validate that the current user has permission to update the analysis

        if not analysis.is_valid():
            raise BadRequestException("Invalid request", analysis.errors)

        scope = analysis.validated_data
        if scope["disaggregations"]:
            disaggregations = self.get_disaggregations(scope["disaggregations"])
        else:
            disaggregations = []
        sectors = self.get_all_sectors_uc.exec(self.repository, None, pk__in=scope["sectors"])
        self.validate_scope_fields(scope, sectors)

        data = {
            "title": scope["title"],
            "objectives": scope["objectives"],
            "start_date": scope["start_date"],
            "end_date": scope["end_date"],
        }

        analysis_updated = self.put_analysis_scope_uc.exec(
            self.repository,
            data=data,
            disaggregations=disaggregations,
            sectors=sectors,
            analysis_id=analysis_id,
        )
        return analysis_updated.to_dict()

    def validate_scope_fields(self, scope, sectors):
        """Validate that the scope contains everything needed and the sectors are not empty"""
        if (
                not all(scope[key] for key in ["title", "objectives", "end_date"])
                or not sectors
        ):
            raise BadRequestException("Missing field")

        if scope["start_date"] and scope["start_date"] >= scope["end_date"]:
            raise BadRequestException("Start date must be before end date")

    def get_disaggregations(self, disaggregations):
        """Retrieve the disaggregations"""
        disaggregations = self.get_all_disaggregations_uc.exec(AnalysisRepositoryImpl(), None, pk__in=disaggregations)
        return [disaggregation.to_dict() for disaggregation in disaggregations]

    def get_analysis(self, workspace_id, query_options: QueryOptions):
        if not workspace_id:
            raise BadRequestException("The workspace is required")
        analyses = self.get_analysis_uc.exec(self.repository, query_options, workspace_id=workspace_id)
        if not analyses:
            raise NotFoundException("No analysis found")
        return analyses.to_dict()

    def get_analysis_by_id(self, analysis_id):
        analysis = self.get_analysis_by_id_uc.exec(
            self.repository, analysis_id
        )
        if not analysis:
            raise NotFoundException("Analysis not found")
        return analysis.to_dict()

    def get_administrative_divisions(self, parent_p_code):
        administrative_divisions = self.get_administrative_divisions_uc.exec(
            self.repository, parent_p_code
        )
        if not administrative_divisions:
            raise NotFoundException("Administrative divisions not found")
        return AdministrativeDivisionSerializer(
            administrative_divisions, many=True
        ).data

    def add_location(self, analysis_id, p_code):
        administrative_division = self.get_administrative_division_by_code_uc.exec(self.repository, p_code)
        if not administrative_division:
            raise NotFoundException("Administrative division not found")
        existing_analysis = self.get_analysis_by_id_uc.exec(self.repository, analysis_id)
        if not existing_analysis:
            raise NotFoundException("Analysis not found")
        found_location = next(
            (loc for loc in existing_analysis.locations if loc.pCode == p_code),
            None
        ) if existing_analysis.locations else None
        if found_location:
            raise BadRequestException("The location is already in the analysis")
        location = self.add_location_uc.exec(self.repository, existing_analysis,
                                             administrative_division)
        return AdministrativeDivisionSerializer(location).data

    def remove_location(self, analysis_id, p_code):
        administrative_division = self.get_administrative_division_by_code_uc.exec(self.repository, p_code)
        if not administrative_division:
            raise NotFoundException("Administrative division not found")
        existing_analysis = self.get_analysis_by_id_uc.exec(self.repository, analysis_id)
        if not existing_analysis:
            raise NotFoundException("Analysis not found")
        found_location = next(
            (loc for loc in existing_analysis.locations if loc.pCode == p_code),
            None
        ) if existing_analysis.locations else None
        if not found_location:
            raise BadRequestException("The location is not present in the analysis")
        self.remove_location_uc.exec(self.repository, existing_analysis, administrative_division)

    def update_steps(self, analysis_id: int, step_ids: List[int]):
        self.get_analysis_by_id(analysis_id)  # if analysis doesn't exist raises 404
        if not step_ids or len(step_ids) <= 0:
            raise BadRequestException("Step ids required")
        steps = self.repository.get_steps_by_ids(step_ids)
        if not steps or len(step_ids) != len(steps):
            raise BadRequestException("All the steps should be valid")
        mandatory_step_ids = self.get_mandatory_step_ids()
        if not set(mandatory_step_ids).issubset(step_ids):
            raise BadRequestException("You can't delete mandatory steps")
        self.update_analysis_steps_uc.exec(self.repository, analysis_id, step_ids)

    def get_steps(self):
        steps = self.get_steps_uc.exec(self.repository)
        dict_steps = [step.to_dict() for step in steps]
        return dict_steps

    def get_mandatory_step_ids(self):
        steps = self.get_steps_uc.exec(self.repository)
        mandatory_steps = [step.id for step in steps if step.mandatory and not step.parentStepId]
        return mandatory_steps
